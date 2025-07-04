const __DEFAULT_LIMIT_SIZE = 15

// @NOTE: if the user has more investments than the default page size,
// `?limit=value | 15`, we should align using backend, through `?order=scope`
function tableOrder(component, count) {
  const scope = component.id.trim();
  if (scope === "") return;

  const url = new URL(document.location.toString());
  const limit = +(url.searchParams.get("limit") || __DEFAULT_LIMIT_SIZE);
  if (count > limit) {
    url.searchParams.set("order_by", scope);
    document.location.href = url.toString();
    return;
  }

  const nodes = [];
  const target = document.querySelectorAll(`[scope="${scope}"]`);
  target.forEach((node) => {
    const value = +node.innerHTML.replace("R$ ", "");
    nodes.push({ parent: node.parentNode, value });
  });
  nodes.sort((a, b) => a.value < b.value);

  const tbody = document.getElementsByTagName("tbody")[0];
  nodes.forEach((node) => tbody.append(node.parent));
}
