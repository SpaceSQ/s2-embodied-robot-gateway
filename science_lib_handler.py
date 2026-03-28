import json
import time

class ScienceLabBusiness:
    def __init__(self, engine):
        self.engine = engine
        self.active_experiment = None

    def load_science_package(self, params):
        """加载科学库：如 'HighSchool_Chem_v1', 'University_Physics_Extreme'"""
        package_name = params.get("package_name")
        experiment_id = params.get("experiment_id")
        
        # 模拟从教材数据库读取参数
        # 实际开发中这里对接一个 JSON 格式的实验教材库
        if package_name == "STEM_Explosion_Test":
            config = {
                "temperature_c": 1500,
                "atmosphere_kpa": 500,
                "gravity_g": 1.0,
                "danger_level": "EXTREME"
            }
        
        # 调用底层的创世引擎
        res = self.engine.set_hyper_environment({
            "suns_mm": params.get("suns_mm"),
            "temperature_c": config["temperature_c"],
            "gravity_g": config["gravity_g"],
            "atmosphere_kpa": config["atmosphere_kpa"]
        })
        
        return f"[HLSL] 科学库 {package_name} 加载成功。实验项目: {experiment_id} 准备就绪。空间已进入净空锁定状态。"

    def run_destructive_test(self, params):
        """执行破坏性测试：如碰撞、爆炸"""
        target_object = params.get("object_id")
        # 触发物理熔毁特效
        return f"[HLSL] 正在对物质 {target_object} 进行破坏性压力测试。正在记录应变数据..."