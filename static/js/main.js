// EcoCollect - Main Client JavaScript

document.addEventListener("DOMContentLoaded", () => {
    // 1. Category selector cards logic for Request Pickup form
    const categoryCards = document.querySelectorAll(".category-selectable-card");
    const categorySelect = document.getElementById("waste_category_select");

    if (categoryCards.length > 0 && categorySelect) {
        // Sync card click to dropdown
        categoryCards.forEach(card => {
            card.addEventListener("click", () => {
                const val = card.getAttribute("data-category");
                categorySelect.value = val;
                
                categoryCards.forEach(c => c.classList.remove("selected", "border-success", "bg-light"));
                card.classList.add("selected", "border-success", "bg-light");
            });
        });

        // Sync dropdown change to cards
        categorySelect.addEventListener("change", () => {
            const currentVal = categorySelect.value;
            categoryCards.forEach(card => {
                if (card.getAttribute("data-category") === currentVal) {
                    card.classList.add("selected", "border-success", "bg-light");
                } else {
                    card.classList.remove("selected", "border-success", "bg-light");
                }
            });
        });
    }

    // 2. Client-side quick filter for Admin Requests Table
    const searchInput = document.getElementById("admin-table-search");
    if (searchInput) {
        searchInput.addEventListener("input", function() {
            const query = this.value.toLowerCase().trim();
            const rows = document.querySelectorAll("#requestsTable tbody tr");
            
            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            });
        });
    }

    // 3. Set minimum pickup date to today
    const pickupDateInput = document.getElementById("pickup_date");
    if (pickupDateInput) {
        const today = new Date().toISOString().split("T")[0];
        pickupDateInput.setAttribute("min", today);
        if (!pickupDateInput.value) {
            pickupDateInput.value = today;
        }
    }
});

/**
 * Copy Request ID to clipboard with user feedback
 */
function copyRequestId(id) {
    if (!id) return;
    navigator.clipboard.writeText(id).then(() => {
        const btn = document.getElementById("btn-copy-id");
        if (btn) {
            const originalHTML = btn.innerHTML;
            btn.innerHTML = `<i class="fa-solid fa-check me-1"></i> Copied!`;
            btn.classList.add("btn-success");
            btn.classList.remove("btn-outline-primary", "btn-outline-secondary");
            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.classList.remove("btn-success");
                btn.classList.add("btn-outline-primary");
            }, 2000);
        } else {
            alert(`Copied ${id} to clipboard!`);
        }
    }).catch(err => {
        console.error("Failed to copy text: ", err);
    });
}

/**
 * Click handler for Smart Guide suggestion pills
 */
function fillGuideSearch(itemText) {
    const input = document.getElementById("guide-item-input");
    const form = document.getElementById("guide-search-form");
    if (input && form) {
        input.value = itemText;
        form.submit();
    }
}
