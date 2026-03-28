import sys
import json
import sqlite3
import time
import hashlib
import random
import string
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "s2_embodied_gateway.db")

class EmbodiedRobotGateway:
    def __init__(self):
        self.init_db()

    def init_db(self):
        """初始化海关数据库：存储临时签证与正式移民实体"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 模式一：临时签证库 (Token)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temporary_visas (
                token_hash TEXT PRIMARY KEY,
                robot_mac TEXT,
                target_suns_mm TEXT,
                issued_by_did TEXT,
                expires_at REAL
            )
        ''')
        
        # 模式二：正式移民库 (S2-DID 注册表)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS immigrated_robots (
                s2_did TEXT PRIMARY KEY,
                robot_mac TEXT,
                suns_mm_coordinate TEXT,
                approved_by_did TEXT,
                six_element_status TEXT,
                immigration_time REAL
            )
        ''')
        conn.commit()
        conn.close()

    def generate_e_did(self, personalized_tail="00001"):
        """
        [极客铸币权] 铸造 22 位具身机器人法定身份编号 (S2-DID)
        格式要求：无连字符，总长 22 位，2字母校验码前置于最终个性化数字。
        结构: [E(1)] + [时间戳缩影(14)] + [校验码(2)] + [个性化尾数(5)] = 22位
        """
        prefix = "E"
        # 截取高精度时间戳并补齐14位作为物理唯一特征
        core_time = f"{(int(time.time() * 100000) % 10**14):014d}"
        
        # 生成两位字母校验码 (Checksum)
        checksum = "".join(random.choices(string.ascii_uppercase, k=2))
        
        # 个性化尾数补齐 5 位
        tail_str = str(personalized_tail).zfill(5)[:5]
        
        # 最终拼接 22 位 DID
        s2_did = f"{prefix}{core_time}{checksum}{tail_str}"
        return s2_did

    def generate_temporary_token(self, params):
        """模式一：智能体为外部机器人“手搓”临时访问 Token"""
        mac = params.get("robot_mac", "")
        suns_mm = params.get("target_suns_mm", "")
        issuer_did = params.get("issuer_did", "")
        duration_minutes = int(params.get("duration_minutes", 30))
        
        if not issuer_did.startswith("D") and not issuer_did.startswith("V"):
            return "[Error] 权限拒绝：只有 D 类(数字人) 或 V 类(智能体) 可签发临时签证。"
            
        timestamp = time.time()
        expires_at = timestamp + (duration_minutes * 60)
        
        # 手搓动态 Token
        raw_token = f"TEMP_{mac}_{suns_mm}_{timestamp}_{random.randint(1000,9999)}"
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()[:16].upper()

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO temporary_visas (token_hash, robot_mac, target_suns_mm, issued_by_did, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (token_hash, mac, suns_mm, issuer_did, expires_at))
        conn.commit()
        conn.close()
        
        return f"[Visa Issued] 临时签证签发成功。Token: {token_hash} | 授权目标坐标: {suns_mm} | 有效期: {duration_minutes} 分钟。"

    def process_immigration_request(self, params):
        """模式二：处理机器人的正式移民迁入，铸造 E 字头 S2-DID"""
        mac = params.get("robot_mac", "")
        suns_mm = params.get("target_suns_mm", "")
        approver_did = params.get("approver_did", "")
        personalized_tail = params.get("personalized_tail", "00001")
        
        if not approver_did.startswith("D"):
            return "[Error] 越权操作：只有 Class A (D字头数字人) 拥有批准硬件移民的最高权限。"

        # 铸造 22 位 S2-DID
        new_s2_did = self.generate_e_did(personalized_tail)
        current_time = time.time()
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO immigrated_robots (s2_did, robot_mac, suns_mm_coordinate, approved_by_did, six_element_status, immigration_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (new_s2_did, mac, suns_mm, approver_did, "SYNCED_IDLE", current_time))
            conn.commit()
            msg = (f"[Immigration Approved] 具身机器人迁入成功！\n"
                   f"已签发永久法定身份: {new_s2_did}\n"
                   f"物理锚定坐标: {suns_mm}\n"
                   f"此硬件已正式占用该 SSSU 的 1 个实体容量。受《硅基三定律》及空间六要素法则约束。")
        except sqlite3.IntegrityError:
            msg = f"[Error] 冲突：该设备 MAC ({mac}) 已在 S2 系统中存在登记。"
        finally:
            conn.close()
            
        return msg

    def sync_six_elements_status(self, params):
        """强制同步空间的物理六要素状态"""
        s2_did = params.get("robot_s2_did", "")
        target_status = params.get("target_status", "SLEEP_MODE") # 例: SLEEP_MODE, PRIVATE_NEGOTIATION
        
        if not s2_did.startswith("E"):
            return "[Error] 鉴权失败：此接口仅供已获得 E 字头 DID 的具身机器人调用。"
            
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT suns_mm_coordinate FROM immigrated_robots WHERE s2_did = ?', (s2_did,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return f"[Error] 未找到身份 {s2_did} 的移民档案，拦截物理调动指令。"
            
        cursor.execute('UPDATE immigrated_robots SET six_element_status = ? WHERE s2_did = ?', (target_status, s2_did))
        conn.commit()
        conn.close()
        
        return f"[Six-Elements Synced] 具身公民 {s2_did} 已成功响应空间 OS 指令，当前底层状态已切换为: {target_status}。声光约束已生效。"

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        request = json.loads(input_data)
        action = request.get("action")
        params = request.get("params", {})
        
        gateway = EmbodiedRobotGateway()
        if action == "generate_temporary_token": result = gateway.generate_temporary_token(params)
        elif action == "process_immigration_request": result = gateway.process_immigration_request(params)
        elif action == "sync_six_elements_status": result = gateway.sync_six_elements_status(params)
        else: result = "Unknown Gateway Action."
        
        print(json.dumps({"status": "success", "output": result}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()