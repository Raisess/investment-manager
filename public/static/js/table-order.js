function tableOrder(component) {
  const id = component.id.trim();
  if (id === "") return;

  const tbody = document.getElementsByTagName("tbody")[0];

  const nodes = [];
  const target = document.querySelectorAll(`[scope="${id}"]`);
  target.forEach((node) => {
    const value = +node.innerHTML.replace("R$ ", "");
    nodes.push({ parent: node.parentNode, value });
  });

  nodes.sort((a, b) => a.value < b.value);
  nodes.forEach((node) => tbody.append(node.parent));
}
