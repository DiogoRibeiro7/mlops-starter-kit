# Security

## Reporting

Report a suspected vulnerability privately through the repository's
[security advisories](https://github.com/DiogoRibeiro7/mlops-starter-kit/security/advisories/new).
If private reporting is unavailable, open an issue asking for a private
contact channel without including exploit details or sensitive data.
Do not submit credentials or private datasets. This project has no guaranteed
response time; the latest release and `main` are the maintained versions.

## Trust Boundaries

- Pickle model artifacts can execute code. Only load models produced by trusted
  jobs. Registry hashes detect accidental modification; they do not authenticate
  a publisher. Never accept arbitrary uploaded model files in the API.
- The prediction service does not implement authentication or TLS. Keep it on a
  trusted network or place an authenticated TLS gateway in front of it. Configure
  request-size limits and rate limits at that gateway.
- Configurations are operator-controlled files. YAML uses safe loading, and
  typed contracts reject unknown options. File paths grant access available to
  the process account; configurations are not a sandbox.
- Containers run as a non-root user. Mount model artifacts read-only for serving.
  Protect the registry and model files with filesystem permissions.
- Keep secrets outside Git. Use environment variables or your deployment's
  secret manager. CI builds use read-only repository permissions and pinned
  actions. The documentation deploy job receives Pages and OIDC write permissions
  only on `main`; pull requests cannot deploy the site.

See scikit-learn's [model persistence guidance](https://scikit-learn.org/stable/model_persistence.html)
for artifact format and environment compatibility considerations.
