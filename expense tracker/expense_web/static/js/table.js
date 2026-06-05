/* table.js — client-side search and sortable columns */

// ── Live search filter ────────────────────────────────────────
const searchInput = document.getElementById('tableSearch');
const tableBody   = document.getElementById('expenseBody');

if (searchInput && tableBody) {
  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    tableBody.querySelectorAll('tr').forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(query) ? '' : 'none';
    });
  });
}

// ── Sortable columns ──────────────────────────────────────────
const table = document.getElementById('expenseTable');

if (table) {
  let sortCol = -1;
  let sortAsc = true;

  table.querySelectorAll('th.sortable').forEach((th, idx) => {
    th.addEventListener('click', () => {
      if (sortCol === idx) {
        sortAsc = !sortAsc;
      } else {
        sortCol = idx;
        sortAsc = true;
        // Clear other arrows
        table.querySelectorAll('th.sortable').forEach(h => {
          h.classList.remove('asc', 'desc');
        });
      }

      th.classList.toggle('asc',  sortAsc);
      th.classList.toggle('desc', !sortAsc);

      const rows = Array.from(tableBody.querySelectorAll('tr'));
      rows.sort((a, b) => {
        const aText = a.cells[idx]?.textContent.trim() ?? '';
        const bText = b.cells[idx]?.textContent.trim() ?? '';

        // Numeric sort for the Amount column (last col)
        const aNum = parseFloat(aText.replace(/[₹,]/g, ''));
        const bNum = parseFloat(bText.replace(/[₹,]/g, ''));
        if (!isNaN(aNum) && !isNaN(bNum)) {
          return sortAsc ? aNum - bNum : bNum - aNum;
        }

        return sortAsc
          ? aText.localeCompare(bText)
          : bText.localeCompare(aText);
      });

      rows.forEach(r => tableBody.appendChild(r));
    });
  });
}
