

@matcher_q.got("option", prompt=question)
async def _(state: T_State, matcher: Matcher, answer: str = ArgPlainText("option")):
    match answer:
        case 1:
            state["step"]=1
        case 2:
            state["step"]=2



@matcher_q.got("step", prompt="step id")
async def _(state: T_State, matcher: Matcher, uid: str = ArgPlainText("uid")):
    if state["step"] == 1:
        print(uid)
    elif state["step"] == 2:
        print()
# =========================================

from nonebot.params import Depends

async def check(state: T_State,key) -> bool:
    return state[key]

@match_q.got("option", prompt=question)
async def call_bot(bot: Bot, state: T_State, matcher: Matcher, option: Message = Arg(), answer: str = ArgPlainText("option")):
    match answer:
        case "1":
            state["if_step1"] == True
        case "2":
            state["if_step2"] == True
            state["if_step1"] == False
            state["pid"] = "null"


@match_q.got("if_step1")
@match_q.got("pid", prompt="请输入pid")
async def _(state: T_State, matcher: Matcher, check:bool = Depends(check("if_step1")),plan_id: str = ArgPlainText("pid")):
        if state["if_step1"] == True:
            print()


@match_q.got("if_step2")
@match_q.got("uid", prompt="请输入uid..")
async def _(state: T_State, matcher: Matcher, order_id: str = ArgPlainText("uid")):
        if state["if_step2"] == True:
            print()