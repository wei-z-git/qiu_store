from nonebot import on_command, get_bot
from nonebot.adapters import Message, Bot
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot.exception import ActionFailed
from nonebot.rule import to_me
import random

async def kicker_group_mem(bot: Bot, matcher: Matcher, event: GroupMessageEvent) -> None:
    """
        踢出不活跃的成员
    """
    gid = int(event.group_id)
    try:
        member_list = await get_bot().call_api("get_group_member_list", group_id=gid, no_cache=True)
        fly_list = order_member_by_time(member_list)
        for member in fly_list:
            qq_num = member['user_id']
            qq_nickname = member['nickname']
            print(qq_num)
            await bot.set_group_kick(group_id=gid, user_id=qq_num, reject_add_request="false")
            await matcher.send("已将 " + str(qq_nickname)+":"+str(qq_num) + " 折跃去冷库！嗖~~\n --消息来自小鸠Joe机器人")

    except ActionFailed as e:
        print(e)
        await matcher.finish(f"机器人权限不足捏")

# 交互式
matcher_call_robot = on_command('call', aliases={'召唤小鸠机器人', '召唤'}, priority=1,
                                permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

# 给ac的
matcher_ac_message = on_command('ac', aliases={'更新音声', '开始直播'}, priority=4)

# # Interative command
question = "洒家来啦~~，哥哥有何吩咐:\n  1.查询冷库食材\n  2.查询冷库食材详细\n  3.发送食材！！！\n  0.退出\n请哥哥选择！\n ---消息来自小鸠Joe机器人"


@matcher_ac_message.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    answer_list = ['ac大笨蛋!', 'a宝小可爱么么哒~', 'a宝别着急, 这就送你去不语家的下水道一日游~',
                   '......', '你个老六', '明年再说', '收到', '等会下播我来接你', '你好，主人不在，有事情请给主人留言，谢谢您使用!','2.有您的支持和肯定，我们会更加努力做到更好，如果亲有不满意的地方请一定及时联系我们哦，不周到的地方还请亲们多多谅解哈。谢谢您的支持']
    random_str = random.choice(answer_list)
    await matcher.send(random_str)


@matcher_call_robot.got("option", prompt=question)
async def call_robot(bot: Bot, matcher: Matcher, event: GroupMessageEvent, option: Message = Arg(), answer: str = ArgPlainText("option")):
    match answer:
        case "1":
            # 1.查询冷库食材
            await search_group_mem_list(bot, matcher, event)
            await matcher_call_robot.finish()
        case "2":
            # 2.查询冷库食材详细
            await search_group_mem_list_detail(bot, matcher, event)
            await matcher_call_robot.finish()
        case "3":
            # 3.发送食材!!!
            await kicker_group_mem(bot, matcher, event)
            await matcher_call_robot.finish()
        case "0":
            # 0.退出
            await matcher_call_robot.finish(f"拜拜了您嘞~")
        case _:
            # 可以使用平台的 Message 类直接构造模板消息
            await matcher_call_robot.reject(option.template("哥哥，泥在说些甚么！洒家听不懂！请再说一遍！ok?"))
