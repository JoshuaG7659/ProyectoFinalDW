fetch("/static/data.json")
.then(function(response){
	return response.json();
})
.then(function(data){
	let placeholder = document.querySelector("#data-output");
	let out = "";
	for(let product of data){
		out += `
			<tr>
				<td>${product.nombre}</td>
				<td>${product.apellido}</td>
				<td>${product.iD_Factura}</td>
				<td>${product.fecha}</td>
                <td>${product.deuda}</td>
				<td>${product.abono}</td>
                <td>${product.saldo}</td>
                <td>${product.mora}</td>
			</tr>
		`;
	}

	placeholder.innerHTML = out;
});