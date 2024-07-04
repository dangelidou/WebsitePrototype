const api = "http://127.0.0.1:5000";

window.onload = () => {

    document.getElementById('product-form').addEventListener('submit', productFormOnSubmit);
    document.getElementById('search-button').addEventListener('click', searchButtonOnClick);

}

searchButtonOnClick = () => {

    preventDefault();  // Prevent the form from submitting and refreshing the page

    const search_name = document.getElementById('search-name').value;
    const res = new XMLHttpRequest();
    res.open("GET", `${api}/search?name=${encodeURIComponent(search_name)}`);

    res.onreadystatechange = () => {
        if (res.readyState == 4 && res.status == 200) {
            const results = document.getElementById("search-results").getElementsByTagName('tbody')[0];
            results.innerHTML = '';  // Clear previous results

            const data = JSON.parse(res.responseText);
            if (data.error) {
                results.innerHTML = `<tr><td colspan="6">${data.error}</td></tr>`;
            } else {
                data.forEach(item => {
                    const row = document.createElement("tr");

                    // Create and append table data elements
                    ['_id', 'name', 'production_year', 'price', 'color', 'size'].forEach(field => {
                        const cell = document.createElement("td");
                        cell.textContent = item[field];
                        row.appendChild(cell);
                    });

                    results.appendChild(row);
                });
            }
        } else if (res.readyState == 4) {
            // Handle the error case
            const results = document.getElementById("search-results").getElementsByTagName('tbody')[0];
            results.innerHTML = `<tr><td colspan="6">An error occurred</td></tr>`;
        }
    };
    res.send();

    // Clear the input field
    document.getElementById('search-name').value = '';
    // )
    // .catch ((error) => {
    //         console.error('Error:', error);
    //         results.innerHTML = `<tr><td colspan="2">An error occurred</td></tr>`;
    //     });


}

productFormOnSubmit = (event) => {

    event.preventDefault();
    let product = {
        id: "",
        name: document.getElementById("name").value,
        production_year: document.getElementById("year").value,
        price: document.getElementById("price").value,
        color: parseInt(document.getElementById("color").value),
        size: parseInt(document.getElementById("size").value)
    };
    fetch(api + '/add-product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(product),
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
    console.log("Product added");

}
