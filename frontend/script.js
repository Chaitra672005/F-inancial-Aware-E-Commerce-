const API = "https://f-inancial-aware-e-commerce.onrender.com";

// Load products
async function loadProducts() {
  let res = await fetch(API + "/products");
  let data = await res.json();

  document.getElementById("products").innerHTML =
    data.map(p => `<p>${p.name} - ₹${p.price}</p>`).join("");
}

loadProducts();

// Checkout
async function checkout() {
  let amount = document.getElementById("amount").value;

  let res = await fetch(API + "/checkout", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({amount: parseFloat(amount)})
  });

  let data = await res.json();

  document.getElementById("result").innerText =
    `Risk: ${data.risk_level} | Score: ${data.risk_score}`;
}

// EMI
async function calculateEMI() {
  let amount = document.getElementById("emi_amount").value;
  let rate = document.getElementById("rate").value;
  let months = document.getElementById("months").value;

  let res = await fetch(`${API}/emi?amount=${amount}&rate=${rate}&months=${months}`);
  let data = await res.json();

  document.getElementById("emi_result").innerText =
    `EMI: ₹${data.emi}`;
}