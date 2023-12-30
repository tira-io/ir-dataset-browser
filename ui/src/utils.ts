async function execute_get(url: string) {
	const response = await fetch(url, {
		method: 'GET',
	})

	if (!response.ok) {
		throw new Error(`Error fetching endpoint: ${url} with ${response.status}`);
	}

	return await response.json()
}

function default_values(): { loading: boolean } {
	return {'loading': false};
}

function inject_response(response: any, obj: any): void {
	const defaults = default_values();

	if (response != null) {
		console.log('response: ' + response)
		for (const k of Object.keys(response)) {
			// @ts-ignore
			// eslint-disable-next-line no-prototype-builtins
			if (response.hasOwnProperty(k) && obj.$data.hasOwnProperty(k)) {
				console.log('copy property ' + k)
				obj.$data[k] = response[k]
			}
		}

		for (const k of Object.keys(defaults)) {
			// eslint-disable-next-line no-prototype-builtins
			if (obj.$data.hasOwnProperty(k)) {
				// @ts-ignore
				obj.$data[k] = defaults[k]
			}
		}
	}
}

export async function get(url: string, obj: any): Promise<any> {
	const response = await execute_get(url);

	inject_response(response, obj);
	return response;
}