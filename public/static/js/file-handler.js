const fileInput = document.getElementById("file");
fileInput.addEventListener("change", handleFileSelection);

async function handleFileSelection(event) {
  const file = event.target.files[0];
  if (!file) {
    throw new Error("File not found");
  }

  if (!file.type.startsWith("application/json")) {
    throw new Error("Unsupported file type");
  }

  const reader = new FileReader();
  reader.onload = async () => {
    const form = new FormData()
    form.append("data", reader.result)

    await fetch("/investment/import", {
      body: form,
      method: "POST",
      redirect: "follow",
    });
    window.location.reload()
  };
  reader.onerror = () => {
    throw new Error("Failed to read the file");
  };
  reader.readAsText(file);
}
