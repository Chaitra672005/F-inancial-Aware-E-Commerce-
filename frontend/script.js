const API = "https://your-backend-url.onrender.com";

// load products
async function loadProducts() {
  let res = await fetch(API + "/products");
  let data = await res.json();

  document.getElementById("products").innerHTML =
    data.map(p => `<p>${p.name} - ₹${p.price}</p>`).join("");
}

loadProducts();

// checkout
async function checkout() {
  let amount = document.getElementById("amount").value;

  let res = await fetch(API + "/checkout", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({amount: parseFloat(amount)})
  });

  let data = await res.json();
  alert("Fraud Status: " + data.fraud_flag);
}

// EMI
async function calculateEMI() {
  let amount = document.getElementById("emi_amount").value;
  let rate = document.getElementById("rate").value;
  let months = document.getElementById("months").value;

  let res = await fetch(`${API}/emi?amount=${amount}&rate=${rate}&months=${months}`);
  let data = await res.json();

  alert("EMI: ₹" + data.emi);
}