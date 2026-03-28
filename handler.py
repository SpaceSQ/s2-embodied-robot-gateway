import sys
import json
import sqlite3
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "s2_tdog_genesis.db")

class TDOGGenesisEngine:
    def __init__(self):
        self.init_db()

    def init_db(self):
        """初始化创世引擎数据库：管理物质生命周期与超限环境状态"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 物质编译器账本
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matter_ledger (
                object_id TEXT PRIMARY KEY,
                suns_mm TEXT,
                object_type TEXT, 
                material_used TEXT,
                entropy_tax REAL,
                status TEXT,
                compiled_at REAL
            )
        ''')
        
        # 超限环境控制台
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hyper_environment_states (
                suns_mm TEXT PRIMARY KEY,
                temperature REAL,
                gravity REAL,
                atmosphere_kpa REAL,
                is_safety_fuse_tripped BOOLEAN,
                last_updated REAL
            )
        ''')
        conn.commit()
        conn.close()

    def compile_matter(self, params):
        """物质编译器：根据 TDOG 理论调动计算材料生成物体"""
        suns_mm = params.get("suns_mm", "")
        object_name = params.get("object_name", "Unknown_Object")
        target_type = params.get("target_type", "Type_3") # Type_1(原子), Type_2(触觉), Type_3(光构架)
        
        material_tech = "Standard_3D_Print"
        entropy_tax = 1.0
        
        if target_type == "Type_3":
            material_tech = "[MR Fluid] 磁流变聚合群瞬间硬化骨架 + 全息投影"
            entropy_tax = 0.1 # 几乎无损耗回收
        elif target_type == "Type_2":
            material_tech = "[DE & SMP] 介电弹性体物理隆起 + 形状记忆聚合物 4D 自组装"
            entropy_tax = 0.5
        elif target_type == "Type_1":
            material_tech = "[Bio-Atomic] 生物墨水/玄武岩粉末 + 极度消耗地球引子"
            entropy_tax = 5.0 # 高熵税

        obj_id = f"OBJ_{int(time.time() * 1000)}"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO matter_ledger (object_id, suns_mm, object_type, material_used, entropy_tax, status, compiled_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (obj_id, suns_mm, target_type, material_tech, entropy_tax, "ACTIVE", time.time()))
        conn.commit()
        conn.close()
        
        return (f"[Matter Compiled] 造物成功！\n"
                f"物品: {object_name} ({obj_id})\n"
                f"真实度: {target_type} | 底层技术: {material_tech}\n"
                f"已锚定至物理坐标: {suns_mm}。")

    def decompile_matter(self, params):
        """反编译：执行衔尾蛇协议，回收物质，扣除熵税"""
        object_id = params.get("object_id", "")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT material_used, entropy_tax FROM matter_ledger WHERE object_id = ? AND status = "ACTIVE"', (object_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return f"[Error] 物质 {object_id} 不存在或已消亡。"
            
        cursor.execute('UPDATE matter_ledger SET status = "DECOMPILED" WHERE object_id = ?', (object_id,))
        conn.commit()
        conn.close()
        
        return (f"[Ouroboros Protocol Executed] 衔尾蛇协议已执行。\n"
                f"物质 {object_id} 已解构。执行热解分离与离心筛选。\n"
                f"已向管廊逆向物流注入回收材料。扣除材料熵税损耗: {row[1]} Credits。")

    def set_hyper_environment(self, params):
        """超限环境发生器：覆写物理常数，受控于亚厘米级防火墙"""
        suns_mm = params.get("suns_mm", "")
        temp = float(params.get("temperature_c", 26.0))
        gravity = float(params.get("gravity_g", 1.0))
        atm = float(params.get("atmosphere_kpa", 101.3))
        
        # 极限参数边界校验
        if not (-270.0 <= temp <= 3000.0): return "[Error] 温度参数超出 -270℃ ~ 3000℃ 极限域。"
        if not (0.0 <= gravity <= 100.0): return "[Error] 重力参数超出 0G ~ 100G 极限域。"
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO hyper_environment_states (suns_mm, temperature, gravity, atmosphere_kpa, is_safety_fuse_tripped, last_updated)
            VALUES (?, ?, ?, ?, False, ?)
        ''', (suns_mm, temp, gravity, atm, time.time()))
        conn.commit()
        conn.close()
        
        return (f"[Hyper-Environment Activated] 超限降临！\n"
                f"坐标: {suns_mm} 边界防火墙已锁定 (误差<1cm)。\n"
                f"当前环境: {temp}℃ | {gravity}G | {atm}kPa\n"
                f"⚠️ 警告: 0.2秒硬件级安全熔断器 (Safety Fuse) 已处于武装监控状态。")

    def emergency_cutoff(self, params):
        """0.2秒安全熔断机制：瞬间清零超限参数"""
        suns_mm = params.get("suns_mm", "")
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE hyper_environment_states 
            SET temperature = 26.0, gravity = 1.0, atmosphere_kpa = 101.3, is_safety_fuse_tripped = True 
            WHERE suns_mm = ?
        ''', (suns_mm,))
        conn.commit()
        conn.close()
        
        return (f"🚨 [SAFETY FUSE BLOWN] 紧急熔断触发！\n"
                f"执行耗时: < 0.2 秒。\n"
                f"空间 {suns_mm} 的所有超限参数已被瞬间卸载。已恢复至 26℃, 1G, 101.3kPa 的安全基线。\n"
                f"环境残留误差: 0℃ / 0dB。生命体安全已保障。")

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        request = json.loads(input_data)
        action = request.get("action")
        params = request.get("params", {})
        
        engine = TDOGGenesisEngine()
        if action == "compile_matter": result = engine.compile_matter(params)
        elif action == "decompile_matter": result = engine.decompile_matter(params)
        elif action == "set_hyper_environment": result = engine.set_hyper_environment(params)
        elif action == "emergency_cutoff": result = engine.emergency_cutoff(params)
        else: result = "Unknown Genesis Action."
        
        print(json.dumps({"status": "success", "output": result}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()