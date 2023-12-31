import {ref} from 'vue'

async function execute_get(url: string, range: string): Promise<any> {
	const response = await fetch(url, {
		method: 'GET',
		headers: {'Range': 'bytes=' + range},
	})

	if (!response.ok) {
		throw new Error(`Error fetching endpoint: ${url} with ${response.status}`);
	}

	return await response.json()
}

function inject_response(response: any, request: any, obj: any): void {
	if (response != null) {
		obj.$data['cache'][request['path']][request['start'] + '-' + request['end']] = response
	}
}

export async function get(request: any, obj: any): Promise<any> {
	let range = request['start'] + '-' + request['end']

	if (obj.$data['cache'][request['path']][range]) {
		return obj.$data['cache'][request['path']][range]
	}

	const response = await execute_get(request['path'], range);

	inject_response(response, request, obj);
	return response;
}

export function updateUrl(topic: string|null = null, dataset: string|null = null, query: string|null = null) {
    var loc = (ref(window.location).value.href + '?').split('?')[0]
    var params = []

    if (topic != null && topic != '') {
        params.push('topic=' + topic)
    }

    if (dataset != null && dataset != '') {
        params.push('dataset=' + dataset)
    }

    if (query != null && query != '') {
        params.push('query=' + query)
    }

	let ret = params.length == 0 ? loc : loc + '?' + params.join('&')
	history.replaceState({'url': ret}, 'ir_datasets explorer', ret)

	return ret
}

export function extractFromUrl(param: string, default_value: string | null = null): string | null {
    let href = (ref(window.location).value.href + '&')

    if (href.indexOf(param + '=') === -1) {
        return default_value;
    }

    return decodeURI(href.split(param + '=')[1].split('&')[0]);
}