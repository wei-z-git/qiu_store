# QIU_store
## 用户手册
1. [用户] 进店导购，`@客服 /老板在吗`
2. [Bot]客服私聊，`商品列表：1.商品名称：鸠鸠侠大战子不语 编号：201222222222, 2... ,请输入需要购买的商品编号...`
3. [用户] 输入商品ID,`编号：201222222222`
4. [Bot] 发送下单链接二维码, `请发送订单号...`
4. [用户] 浏览器扫码打开下单链接，下单，发送订单号给bot客服,`88888888`
5. [Bot] 客服会在校验后发货

## Todos
- [ ] 新用户欢迎信息，包含导购帮助信息(不知道如何实现)
### 商品购买
- [x] 私信创建会话
- [x] 私信会话中，主动发送导购帮助信息和商品信息
- [x] 私信会话中，根据用户输入商品id，被动发送商品下单链接和商品信息
- [x] 私信会话中，用户输入订单号，被动发送最终商品

### 商品筛选查询

### 其他
- [x] 优化召唤命令，将所有功能集中
- [ ] 异常情况处理优化
- [x] 下单地址格式化
## Configs
.env

## 启动
```
docker run -d --name [机器人name] \ 
-e HOST="0.0.0.0" \
-e PORT="80" \
-e QQGUILD_BOTS="[ { \"id\": \"xxx\", \"token\": \"xxx\", \"secret\": \"xxx\", \"intent\": { \"guild_messages\": true, \"at_messages\": false,\"direct_message\":true } } ]" \
-e QQGUILD_IS_SANDBOX="false" \
-e AIFADIAN_USER_ID="xxx" \
-e AIFADIAN_TOKEN="xxx" \
-e GOODS_SECRETS_URL="xxx"
-v /tmp/data:/app/data \
-p 8083:80 \
registry.jihulab.com/nonebot2-wei-z/qiu_store:latest
```
