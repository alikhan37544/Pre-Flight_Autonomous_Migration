# Rules research: code rules, review rules, and APD constraints

This document maps every rule in PreFlight's code and review packs to its
detection pattern, cloud target, refactor strategy, claim strength, and public
citation where one exists. It is a research record, not a vendor rule book.

The rule sources are:

- `rules/codebase_rules.yaml` — 16 code rules, 11 categories, Guardian blocking
  severities `error`;
- `rules/review_rules.yaml` — 11 review rules, of which 8 produce the 8 review
  rule groups in the `R-DEMO-001` gate register;
- `rules/mapping_rules.yaml` and the APD documentation below — the APD naming
  and codegen constraints.

All citations were checked on **11 November 2026**. Public page titles and
quotations were verified by fetching the page. Where a rule body sits behind a
Guidewire login, only the public index entry, ID, and title were verified; the
body is labelled **gated**.

---

## 1. Claim-strength vocabulary

| Label | Meaning in PreFlight | What it is not |
|---|---|---|
| `verified-id` | A public Guidewire page lists the standard ID and exact title; the rule body may be gated. | Not a claim that the full standard text was read or that PreFlight reproduces it. |
| `verified-policy` | An exact public Guidewire policy or hardening statement supports the pattern; no standard ID is bound. | Not a Cloud Standard ID and not a pass/fail assessment. |
| `verified-doc` | An exact public product-documentation behavior is reproduced, with a quoted example. | Not a Cloud Standard and not a statement about every release. |
| `secondary` | A public secondary source (for example a Guidewire developer blog) describes the pattern. | Not a standard, not a policy, and not a substitute for the target release's rule pack. |
| `heuristic` | PreFlight's own structural detector. The pattern is plausible and reviewable, but no vendor rule was verified for it. | Not a Guidewire rule, not a Cloud Standard, and not proof of a cloud blocker. |

Only two `IS-*` IDs are bound anywhere in the packs:

- `IS-TLS-1238` — **Use of Direct SQL Calls to Access a Database**;
- `IS-TLS-1191` — **Hidden Package Reference**.

No other `IS-*` ID is bound to a rule. The public hardening index also lists
`IS-TLS-1022` (**Deprecated API Usage**), but PreFlight does **not** bind its
broader removed-runtime-API family to that ID.

---

## 2. The 16 code rules

“Citation” keys refer to the source table in section 5. “None verified” means no
rule-specific public source was found; the rule remains a labelled heuristic.

| Rule | Detection pattern (implementation) | Cloud target | Refactor strategy | Claim | Citation |
|---|---|---|---|---|---|
| `PF-CODE-SQL-001` | `java.sql.*`, `javax.sql.*`, `DriverManager.getConnection`, `createStatement`, `prepareStatement`, `executeQuery/Update/Batch` | Gosu Query or application API for synchronous reads; application APIs for writes; Cloud Data Access only for analytics/export | Remove JDBC imports and calls; add a typed Gosu Query draft | `verified-id` `IS-TLS-1238` | G1, G3, G6 |
| `PF-CODE-SQL-002` | `executeQuery/Update` with string concatenation; `SELECT/UPDATE/DELETE/INSERT` literals concatenated | Typed Gosu Query or application API | Quarantine the handwritten statement; route through typed data access with bound parameters | `heuristic` | G3 (general SQL-injection guidance only) |
| `PF-CODE-SQL-003` | Any `.sql` file in the extension bundle (`detection.kind: always` with `.sql`) | Gosu Query / application API, or a Cloud Data Access export model for analytics | Quarantine the raw script; move the operation behind a supported data API | `heuristic` | G2 (direct database modification is prohibited; file-level detection is ours) |
| `PF-CODE-MSG-001` | `gw.plugin.messaging`, `MessageTransport`, `javax.jms`, `jakarta.jms`, `com.ibm.mq`, `<messageTransport/jms/mq>`, `MessageDestination` | App Events webhook or Integration Gateway route | Remove the transport plugin; generate an App Events publication draft and a Gateway delivery route | `secondary` | G9, G18 |
| `PF-CODE-SRV-001` | `javax.servlet`, `jakarta.servlet`, `extends HttpServlet`, `@WebServlet`, `<servlet>` | Cloud API extension endpoint or Integration Gateway route | Remove the servlet surface; generate a Cloud API extension YAML and a JAX-RS resource draft | `verified-policy` | G1 |
| `PF-CODE-API-001` | `javax.ejb`, `java.rmi`, `javax.naming`, `javax.xml.rpc`, `sun.misc.Unsafe`, `org.apache.commons.httpclient`, `javax.activation` | Supported platform API or Integration Gateway | Remove the unsupported call; record the supported replacement family | `verified-policy` | G1, G8 |
| `PF-CODE-API-002` | `gw.internal.*`; `com.guidewire.*` excluding `com.guidewire.public.*` | Supported public Guidewire API | Remove the internal import/usage; replace with a public API or drop the dependency | `verified-id` `IS-TLS-1191` | G1, G7 |
| `PF-CODE-SEC-001` | Secret-assignment detector on comment-masked, value-preserving text | Cloud secret manager binding | Replace the literal with a secret/environment binding and generate a secret-reference descriptor; redact the diff | `verified-id` `SEC00-G` | G2, G4 |
| `PF-CODE-SEC-002` | `MessageDigest` with `MD5`/`SHA-1`; `Cipher` with `DES`/`ECB`; `DES…/NoPadding` | Platform-managed FIPS-validated encryption | Replace with SHA-256/AES-GCM or a platform primitive; do not carry custom encryption | `heuristic` | G2 (platform-encryption policy only) |
| `PF-CODE-MT-001` | Static non-`final` field declaration, including `static var` | Tenant-scoped service state or managed cache | Remove `static`; add a tenant-isolation review note | `heuristic` | None verified |
| `PF-CODE-MT-002` | `new Thread`, `Executors`, `System.exit`, `Runtime.exec`, absolute `new File`/`Paths.get`, `System.get/setProperty` | Platform scheduler, configuration service, or Integration Gateway | Remove the local-process/thread/filesystem assumption; route to a managed service | `heuristic` | None verified |
| `PF-CODE-TX-001` | `commit()` inside a `runWithNewBundle` block | Managed bundle transaction | Remove the explicit commit; let the bundle boundary manage the transaction | `secondary` | G14 |
| `PF-CODE-EXC-001` | Empty `catch` block | Explicit failure handling | Recover, rethrow with context, or record a typed failure | `verified-id` `ERR00-G` | G5 |
| `PF-CODE-APD-001` | XML product-template type name above the effective APD limit (default 24) | Codegen `nameOverride` plus regenerated endpoints | Generate a codegen `nameOverride` mapping the truncated visualized name to the installed name | `verified-doc` | G10, G11, G12 |
| `PF-CODE-GUNIT-001` | Database calls in a GUnit test | Pure GUnit with mocked seams | Move database assertions to an integration test; keep the unit test pure | `heuristic` | None verified |
| `PF-CODE-LOG-001` | Sensitive field written to a log or standard output | Structured logging with redaction | Remove or redact the value before logging | `heuristic` | G2 (general security guidance only) |

### 2.1 Notes on individual rules

- **SQL-001** is the strongest data-access claim: the public hardening index
  lists `IS-TLS-1238` and the public Gosu guidance states that JDBC is not
  supported on Guidewire Cloud. The standard body is gated.
- **SQL-002** is not a separate vendor rule. It is a PreFlight heuristic built
  on the same SQL-injection concern; the public `INJ00-G` page is about
  parameterization, not about a cloud-specific dynamic-SQL standard.
- **SQL-003** is a file-level heuristic. The public policy says direct database
  modification via SQL is prohibited; it does not say every `.sql` file is
  deployed application logic. The rule is intentionally conservative.
- **MSG-001** is `secondary`: the App Events overview describes the replacement
  pattern and the limitations of legacy message-transport plugins, but PreFlight
  has not verified a named standard that prohibits every JMS/MQ plugin.
- **SRV-001** is `verified-policy`, not `verified-id`. The public statement is:
  “The use of custom servlets is not a recommended practice. All integrations
  should be implemented using the approved REST API framework.”
- **API-001** is a family-level policy heuristic. The public index lists
  `IS-TLS-1022` (Deprecated API Usage); PreFlight's regex family is broader and
  is deliberately not mapped to that ID.
- **API-002** binds the public `IS-TLS-1191` title. The standard body is gated.
- **SEC-001** binds `SEC00-G` (Gosu secure coding), not a Cloud Standard. The
  public data-security guidance independently says secrets must never be stored
  in plaintext in configuration, source, or runtime properties.
- **SEC-002** is a heuristic. The public policy supports platform-managed,
  FIPS-validated encryption and rejects custom schemes; it does not publish an
  exhaustive weak-algorithm list.
- **MT-001** and **MT-002** are PreFlight heuristics. They are plausible
  cloud-runtime risks, but no public Guidewire rule specific to static fields or
  local threads was verified. Do not present them as vendor findings.
- **TX-001** is `secondary`: a Guidewire developer blog names explicit commits in
  `runWithNewBundle` as a CUE finding. It is not a public standard.
- **EXC-001** binds `ERR00-G`. The public guidance also treats printing a stack
  trace as equivalent to suppressing the exception, which supports `LOG-002`.
- **APD-001** is `verified-doc`. The public page says type names are limited to
  24 characters, gives the `WCRetroRatingLetterOfCredit` truncation example, and
  prescribes `nameOverride` plus endpoint regeneration.
- **GUNIT-001** and **LOG-001** are heuristics. No rule-specific public source
  was verified.

---

## 3. The review rules

### 3.1 The eight rule groups observed in `R-DEMO-001`

The feature migrator opens **one gate per open rule family**, not one gate per
finding. On `PA-VEH-01`, 24 open findings collapse into 8 rule groups, each with
3 findings. Add the 3 open assumptions and the result is 11 gates.

| Review rule | Pattern | Demo gate | Severity | Cloud target / refactor strategy | Claim | Citation |
|---|---|---|---|---|---|---|
| `PF-GW-SQL-001` | Direct JDBC or SQL: `java.sql` types, `javax.sql`, `DriverManager.getConnection` | 3 findings | high | Gosu Query or application API for synchronous reads; CDA only for analytics/export; replace direct JDBC | `verified-id` `IS-TLS-1238` | G1, G3, G6 |
| `PF-GW-SEC-001` | Hard-coded secret (secret-assignment detector) | 3 findings | high | Secret manager binding; rotate the exposed value | `verified-id` `SEC00-G` | G2, G4 |
| `PF-GW-PKG-001` | Hidden/internal package: `gw.internal.*`, non-public `com.guidewire.*` | 3 findings | high | Supported public API; remove the internal import | `verified-id` `IS-TLS-1191` | G1, G7 |
| `PF-GW-EXC-001` | Empty catch block | 3 findings | medium | Explicit failure handling; recover or rethrow with context | `verified-id` `ERR00-G` | G5 |
| `PF-GW-TX-001` | Explicit `commit()` inside `runWithNewBundle` | 3 findings | medium | Managed bundle transaction; remove the commit | `secondary` | G14 |
| `PF-GW-SRV-001` | `javax.servlet`, `HttpServlet`, `@WebServlet` | 3 findings | medium | Cloud API extension or Gateway route; remove the servlet | `verified-policy` | G1 |
| `PF-GW-NAM-001` | Product-template type name over 24 characters | 3 findings | high | Codegen `nameOverride`; regenerate endpoints | `verified-doc` | G10, G11 |
| `PF-GW-GUNIT-001` | Database access in a pure GUnit test | 3 findings | medium | Pure GUnit with mocked seams; move DB assertions to an integration test | `heuristic` | None verified |

### 3.2 Three further review rules in the pack

These rules are defined in `rules/review_rules.yaml` but did not produce a gate
in the demo slice. They are listed so the pack is not misrepresented as
eight rules total.

| Review rule | Title / detection | Claim | Citation |
|---|---|---|---|
| `PF-GW-LOG-001` | Sensitive field written to a log | `heuristic` | G2 (general only) |
| `PF-GW-LOG-002` | `System.out/err`, `printStackTrace`, bare `print` | `heuristic` | G5 |
| `PF-GW-SBT-001` | Standards Based Template readiness marker (`sbt_marker`) | `heuristic` | G15 |

`PF-GW-SBT-001` is a synthetic marker heuristic. The Olos release note says
lines built from a Standards Based Template “cannot be converted to APD-managed
lines at this time”; PreFlight flags the marker, not an official SBT assessment.

---

## 4. APD constraints

APD is where a naming detail becomes a compile failure. The facts below are
public; the 20-character scenario is a PreFlight simulation, not a published
Guidewire release note. The governing rule, `PF-CODE-APD-001`, is
**`verified-doc`**; its cloud target is a codegen `nameOverride` with regenerated
endpoints, its refactor strategy is `apd_name_override`, and its citations are
G10, G11, and G12. The 24-character limit is a type-name limit, not a universal
limit on every field or label.

| Constraint | Public evidence | PreFlight behavior |
|---|---|---|
| Type names are limited to **24 characters** | “type names are limited to 24 characters” (G10) | `PF-CODE-APD-001` uses `name_limit: 24` and scans XML product templates. |
| APD truncates names above the limit on import | The page describes truncation of the visualized product name (G10) | The rule reports the type name and length; it does not silently rewrite the template. |
| Truncation causes endpoint compile errors | Mapping/updater endpoints reference names that no longer match the installed entity (G10) | Architect drafts a codegen `nameOverride` and a review note. |
| `nameOverride` maps the truncated visualized name to the installed name | Example: `WCRetroRatingLetterOfCre: nameOverride: WCRetroRatingLetterOfCredit` (G10) | The generated draft uses the 24-character truncated key and the full installed name as the value. |
| Endpoints must be regenerated after the override | G10 instructs the reader to regenerate LOB-specific endpoints | The draft is not compiled or regenerated; a human must run the real codegen. |
| `_gen` files are codegen output and must not be edited | “Do not modify codegen output files directly” (G12) | `_gen` is excluded from targets; only `_ext` drafts are produced. |
| `_ext` files are LOB extension files | `<productCode>_ext` naming (G12) | Draft targets use `_ext` paths under `config/integration/...`. |
| `nameOverride` is for Cloud Retrofit **without** APD App | “The nameOverride property should be used only for Cloud Retrofit without APD App. For Cloud Retrofit with APD App or APD conversion, use schemaPropertyName.” (G11) | PreFlight models the non-APD Cloud Retrofit path. Do not reuse its field-level advice for the APD App path. |
| A future release could tighten the limit | No public 2027.04 note was verified; the 20-character limit is a PreFlight scenario | `GWCP-APD-NAMING-2027.04` sets an effective limit of 20 and regenerates overrides at 20 characters. Label it a simulation. |

**Demo detail.** The review run has three open `PF-GW-NAM-001` findings for
synthetic types of 37, 37, and 36 characters. The codebase lab's Cascade draft
uses a 24-character key (`CascadePersonalAutoRatin`) with the full installed
name as the override. Harbor uses `HarborHomeownersWindMiti`. These drafts are
synthetic illustrations of the documented mechanism, not compiled products.

---

## 5. Public sources

| Key | Source | URL | Verification |
|---|---|---|---|
| G1 | Application and Development Security (Guidewire Security hardening guidance) | https://docs.guidewire.com/security/hardening-guidance-for-insurancesuite/application-and-development-security | Public page fetched; servlet quote and standard-index links verified. |
| G2 | Data Security and Governance (Guidewire Security hardening guidance) | https://docs.guidewire.com/security/hardening-guidance-for-insurancesuite/data-security-and-governance | Public page fetched; secrets, platform encryption, and direct-SQL quotes verified. |
| G3 | INJ00-G: Prevent SQL Injection | https://docs.guidewire.com/security/gosu-secure-coding-guidelines/INJ00-G | Public page fetched; “JDBC is not supported on Guidewire Cloud” verified. |
| G4 | SEC00-G: Do Not Hardcode Secrets | https://docs.guidewire.com/security/gosu-secure-coding-guidelines/SEC00-G | Public page fetched; title and scope verified. |
| G5 | ERR00-G: Do Not Suppress Exceptions | https://docs.guidewire.com/security/gosu-secure-coding-guidelines/ERR00-G | Public page fetched; empty-catch and stack-trace guidance verified. |
| G6 | IS-TLS-1238: Use of Direct SQL Calls to Access a Database | https://docs.guidewire.com/cloud/standards/latest/Tools/Standard-IS-TLS-1238-UseOfJDBC.html | ID and title verified from the public index; body is gated (login page returned). |
| G7 | IS-TLS-1191: Hidden Package Reference | https://docs.guidewire.com/cloud/standards/latest/Tools/Standard-IS-TLS-1191-HiddenPackageReference.html | ID and title verified from the public index; body is gated. |
| G8 | IS-TLS-1022: Deprecated API Usage | https://docs.guidewire.com/cloud/standards/latest/Tools/Standard-IS-TLS-1022-DeprecatedAPIUsage.html | ID and title verified from the public index; body is gated. Not bound to a PreFlight rule. |
| G9 | App Events (InsuranceSuite Cloud Integration) | https://docs.guidewire.com/education/cloud-integration-basics/latest/docs/integration_cloud_basics/appevents_overview | Public page fetched; replacement pattern and delivery guarantees verified. |
| G10 | Correcting Cloud API LOB endpoint compile errors | https://docs.guidewire.com/cloud/is/202607/cloudapica/cloudAPI/LOBEndpoints/generating-LOB-endpoints/c_correcting_compile_errors.html | Public page fetched; 24-character limit, truncation, and `nameOverride` example verified. |
| G11 | Codegen config file syntax | https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/03-codegen-config-files/c_codegen_config_file_syntax.html | Public page fetched; `nameOverride`, `schemaPropertyName`, and the APD-App restriction verified. |
| G12 | Files that define LOB-specific endpoints | https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/01-generating-LOB-endpoints/c_files_that_define_lob_specific_endpoints.html | Public page fetched; `_gen` read-only and `_ext` naming verified. |
| G13 | Cloud Retrofit with APD App | https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/01-generating-LOB-endpoints/cloud-retrofit-with-apd.html | Public page fetched; APD-assisted flow and “Delete the product from the APD App” verified. |
| G14 | Lessons from Guidewire Cloud Migrations (Guidewire developer blog) | https://www.guidewire.com/resources/blog/developers/lessons-from-guidewire-cloud-migrations-de-risking-the-move-to-saas-via-guidewire-cloud | Public page fetched; explicit-commit and callback-servlet statements verified. Secondary source. |
| G15 | What's new in Cloud Platform for Olos | https://docs.guidewire.com/cloud/olos/whatsnew/topics/gwcp-release_highlights.html | Public page fetched; SBT conversion limitation verified. |
| G16 | List of APIs in Cloud API | https://docs.guidewire.com/cloud/bc/202507/cloudapibf/cloudAPI/topics/101-Fund/01-overview-of-Cloud-API/c_list-of-APIs-in-Cloud-API.html | Public page fetched; major-version path semantics verified. |
| G17 | Manage secrets (Guidewire Cloud Platform) | https://docs.guidewire.com/cloud/gcc-guide/insurer-developer/latest/manage-secrets | Public page fetched; secrets app behavior verified. |
| G18 | Integration Framework (Guidewire) | https://www.guidewire.com/developers/developer-tools-and-guides/integration-framework | Public page fetched; App Events and Integration Gateway roles verified. |
| G19 | Manage mTLS configurations (Guidewire Cloud Platform) | https://docs.guidewire.com/cloud/gcc-guide/insurer-developer/latest/manage-certificates | Public page fetched; mTLS behavior verified. |
| G20 | PolicyCenter Cloud API Developer Guide | https://docs.guidewire.com/cloud/pc/202603/cloudapica/ | Public page fetched; endpoint-generation documentation index verified. |

---

## 6. What we do not claim

1. **We do not claim an official Cloud Assurance result.** PreFlight is not
   Cloud Assurance, does not run the official threshold, and does not produce a
   pass, fail, score, or certification.
2. **We do not claim the full Cloud Standards corpus.** Only `IS-TLS-1238` and
   `IS-TLS-1191` are bound by ID. Their bodies are gated. A public title is not
   the full rule text.
3. **We do not invent `IS-*` IDs.** If a rule has no verified ID, it is labelled
   `heuristic`, `secondary`, `verified-policy`, or `verified-doc` instead.
4. **We do not claim a heuristic is a vendor rule.** Regex detection is not an
   AST, compiler, data-flow engine, or official inspection.
5. **We do not claim every cloud blocker is covered.** The packs cover 16 code
   families and 11 review rules; a real estate will contain patterns and
   framework behavior outside them.
6. **We do not claim APD conversion or Cloud Retrofit delivery.** The APD
   material is a naming/codegen constraint; the lab drafts a `nameOverride` and
   a note. It does not convert a product or regenerate production endpoints.
7. **We do not claim custom servlets are absolutely prohibited.** The public
   policy says they are “not a recommended practice”; the rule is
   `verified-policy`, not a hard standard ID.
8. **We do not claim the weak-crypto list is a Guidewire standard.** The
   platform-encryption policy is public; the specific MD5/SHA-1/DES/ECB regex
   list is PreFlight's heuristic.
9. **We do not claim static-state, local-thread, GUnit, or logging rules are
   official findings.** They are labelled `heuristic` and require human review.
10. **We do not claim generated drafts compile.** No Gosu compiler, Java
    compiler, Guidewire runtime, or tenant is invoked. Candidate entities in
    generated Gosu need domain confirmation.
11. **We do not claim `nameOverride` is right for every APD path.** The public
    docs restrict field-level `nameOverride` to Cloud Retrofit without APD App;
    APD App and APD conversion use `schemaPropertyName`. PreFlight models the
    non-APD path only.
12. **We do not claim the 2027.04 scenarios are published releases.** They are
    PreFlight simulations of a mid-migration release change. The 20-character
    limit is not a verified Guidewire release note.
13. **We do not claim the public citations are endorsements.** A link to a
    Guidewire page does not mean Guidewire reviewed, approved, or certified
    PreFlight.
14. **We do not claim the demo numbers are customer results.** Cascade Mutual
    and Harbor P&C are synthetic. The repo contains no customer data.
15. **We do not claim release permanence.** Public docs change; re-verify the
    24-character limit, codegen syntax, and standard titles against the target
    release before planning work.

---

## 7. Research gaps and unverified citations

| Item | Status | Handling in PreFlight |
|---|---|---|
| `IS-TLS-1238` body | Gated; only public ID/title verified | Rule is `verified-id`; message paraphrases the public title and policy, not the gated body. |
| `IS-TLS-1191` body | Gated; only public ID/title verified | Same. |
| `IS-TLS-1022` body | Gated; public index title verified | Not bound to any PreFlight rule. |
| Dynamic SQL cloud-specific standard | No rule-specific public source found | `PF-CODE-SQL-002` is `heuristic`; cited to general SQL-injection guidance. |
| Raw `.sql` file rule | No rule-specific public source found | `PF-CODE-SQL-003` is `heuristic`; cited to the general direct-database policy. |
| Weak-crypto algorithm list | No public Guidewire list found | `PF-CODE-SEC-002` is `heuristic`; policy citation is general. |
| Static mutable state | No public Guidewire rule found | `PF-CODE-MT-001` is `heuristic`; no citation asserted. |
| Local thread/process/filesystem | No public Guidewire rule found | `PF-CODE-MT-002` is `heuristic`; no citation asserted. |
| GUnit database coupling | No public rule-specific source found | `PF-CODE-GUNIT-001` is `heuristic`; no citation asserted. |
| Sensitive logging | No public rule-specific source found | `PF-CODE-LOG-001` is `heuristic`; the data-security page is general context only. |
| `PF-GW-SBT-001` detection | Public SBT limitation verified; the marker detector is PreFlight's | Rule remains `heuristic`; it flags `standardsBasedTemplate="true"`. |
| Guidewire blog (TX-001) | Public secondary source verified | Labelled `secondary`, never presented as a standard. |

The research result is intentionally conservative: a rule with a weaker claim
is still useful for review, but it must not borrow the authority of a standard
it cannot cite.
