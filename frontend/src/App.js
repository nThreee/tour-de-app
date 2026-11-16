(function () {
  const tableContainer = document.getElementById("product-list");
  const jmenokontejner = document.getElementById("jmena-list");

  let editingId = null;

  const { setEditing, resetForm } = initProductForm({
    onSubmit: async ({ id, name, cost }) => {
      if (id !== null) {
        await updateProduct(id, { name, cost });
        resetForm();
        editingId = null;
      } else {
        await createProduct({ name, cost });
      }
      loadProducts();
    },
  });

  async function checkHealth() {
  try {
    const response = await fetch("/api/v1/health");
    const data = await response.json();

    if (response.ok && data.status === "ok") {
      document.getElementById("health-status").textContent = "Status: OK";
    }
  } catch (e) {
    console.error("Health check failed:", e);
  }
}

  async function loadProducts() {
    try {
      const data = await getProducts();
      renderProductTable(tableContainer, data, {
        onEdit: (product) => {
          editingId = product.id;
          setEditing(product);
        },
        onDelete: async (id) => {
          await deleteProduct(id);
          if (editingId === id) {
            resetForm();
            editingId = null;
          }
          loadProducts();
        },
      });
    } catch (e) {
      console.error("Failed to load products:", e);
    }
  }

  async function loadJmena() {
    try {
      const data = await getJmena();
      jmenokontejner.innerHTML = "";

      for (let i = 0; i < data.length; i++) {
        jmenokontejner.innerHTML += data[i].jmeno;
      }
    } catch (e) {
      console.error("Failed to load jmena:", e);
    }
  }

  loadProducts();
  checkHealth();
  loadJmena();
})();
