import {
  GITHUB_REPO,
  SITE_URL,
  VOLATILE_RULE,
  type ErpFacts,
} from "../lib/types.js";

export function sourcesAndMethod(data: ErpFacts) {
  return {
    checked_on: data.checked_on,
    certainty_levels: data.certainty_levels,
    rule: VOLATILE_RULE,
    repository: GITHUB_REPO,
    site: SITE_URL,
  };
}
