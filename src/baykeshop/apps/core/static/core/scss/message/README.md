<font size="6">Message.js</font>

**插件描述：**一款优雅的原生JS页面消息提示插件，兼容性良好，无任何依赖。



**声明：**此插件非笔者原创，笔者只做了部分内容的修改，以符合个人需求。以下为原插件来源信息：

- 原作者：或许吧（jesseqin）

- 转载地址：https://www.jq22.com/jquery-info23550

![message.js](assets/intro-zh.jpg)

**使用：**

**html引入：**

```html
<link rel="stylesheet" href="./message.min.css">
<!-- your html -->
<script src="./message.min.js"></script>
<script>
    var configs = {};
    // configs 为配置参数，可省略
    Qmsg.info("这是提示消息",configs);
</script>
```



**全局配置**

在引入message.js之前可以通过全局变量 QMSG_GLOBALS.DEFAULTS 来进行配置

```javascript
window.QMSG_GLOBALS = {
    DEFAULTS: {
        showClose:true,
        timeout: 5000
    }
}
```

或者通过`Qmsg.config({})`来动态修改全局配置:

```javascript
Qmsg.config({
    showClose:true,
    timeout: 5000
})
```

所有支持的配置信息如下:

| **参数名 ** | **类型 ** | **描述 **                                 | **默认 ** |
| ----------- | --------- | ----------------------------------------- | --------- |
| showClose   | Boolean   | 是否显示关闭图标                          | false     |
| autoClose   | Boolean   | 是否自动关闭                              | true      |
| timeout     | Number    | 自动关闭时，消息的持续显示时间，单位 ms   | 2000      |
| content     | String    | 提示的消息内容                            | ''        |
| onClose     | Function  | 关闭时的回调函数                          | null      |
| html        | Boolean   | 是否将内容作为 html 渲染                  | false     |
| maxNums     | Number    | 页面中最多显示消息(autoClose: true)的数量 | 5         |



**Qmsg支持的方法**

```javascript
Qmsg.info()
Qmsg.warning()
Qmsg.error()
Qmsg.success()
Qmsg.loading()
```

以上方法均可传递 1-2 个参数，如下：

```javascript
Qmsg.loading("我是加载条");
Qmsg.info("给你个眼神，你懂得",{
    showClose:true,
    onClose:function(){
        console.log('我懂了')
    }
})
Qmsg.error({
    content:"1+1=3",
    timeout:5000
})
```

**注意：**`Qmsg.loading()`默认设置`autoClose = false`，一般来说需要手动关闭：

```javascript
var loadingMsg = Qmsg.loading('我是加载条');
// do something
loadingMsg.close();
```

如需要自动关闭则需要如下调用:

```javascript
Qmsg.loading("我是加载条",{
    autoClose:true
})
// 或者
Qmsg.loading({
    autoClose:true,
    content:"我是加载条"
})
```

**Qmsg.closeAll()**

关闭所有消息，包括`autoClose = false`的消息

```javascript
var aMsg = Qmsg.info("这是个info消息")
```

**close()**

关闭当前消息，会触发`onClose`回调函数。

```javascript
aMsg.close()
```

**destroy()**

销毁消息，不会触发`onClose`回调函数。

```javascript
aMsg.destroy()
```

