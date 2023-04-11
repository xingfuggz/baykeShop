function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// axios发送请求
function request(config) {
    const instance = axios.create({
        baseURL: '',
        timeout: 5000,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    });
    
    // 拦截请求
    instance.interceptors.request.use(
        config => {
            // console.log(config)
            return config;
        }, err => {
            console.log(err);
        })
    
    // 拦截响应
    instance.interceptors.response.use(
        res => {
            return res
        }, err => {
            // console.log(err.response.status)
            if (err.response.status == 400){
                data = JSON.stringify(err.response.data)
                alert(data)
            }
            return err.response
        }
    )

    return instance(config);
}