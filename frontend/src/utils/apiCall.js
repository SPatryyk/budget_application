export async function APICall(url, method, headers, body, cb) {
    let respContent = {}
    respContent.method = method
    if (headers) {
        respContent.headers = headers
    }
    if (body) {
        respContent.body = body
    }
    let response = await fetch('https://budget-application-hkvk.onrender.com/api'+url, respContent)
    cb(response.status, response)
}