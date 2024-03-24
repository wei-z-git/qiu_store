import nonebot
from nonebot.adapters.qqguild import Adapter as qqguild_Adapter



nonebot.init(driver="~fastapi+~httpx+~websockets",command_start={"", ""})

driver = nonebot.get_driver()
driver.register_adapter(qqguild_Adapter)


nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()