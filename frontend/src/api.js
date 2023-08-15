// api.js
async function getDetails(firstUrl, secondUrl) {
	try {
		const response = await fetch(
			`http://localhost:5000/getGraph?url1=${firstUrl}&url2=${secondUrl}`,
			{
				headers: {
					'Access-Control-Allow-Origin': '*',
				},
			}
		);
		const data = await response.json();
		return data;
	} catch (error) {
		throw new Error('Failed to fetch graph data');
	}
}

export { getDetails };
