import type { ErpFacts } from "../lib/types.js";
import { fold, formatOdooChange, takeFacts } from "../lib/helpers.js";

export function odoo20Changes(
  data: ErpFacts,
  args: { area?: string },
) {
  const areaFilter = args.area ? fold(args.area) : undefined;
  const selected = areaFilter
    ? data.odoo_20_changes.filter((c) => fold(c.area) === areaFilter)
    : data.odoo_20_changes;

  return {
    changes: takeFacts(selected).map(formatOdooChange),
  };
}
