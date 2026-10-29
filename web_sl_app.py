import streamlit as st
import math

st.set_page_config(page_title="WEB SL 智能选型助手", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; color: #2e7d32; }
    .warning-box { background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107; margin-bottom: 20px;}
    .vol-box { background-color: #e3f2fd; padding: 15px; border-radius: 5px; border-left: 5px solid #1976d2; margin-bottom: 20px;}
    .pass-box { background-color: #e8f5e9; padding: 15px; border-radius: 5px; border-left: 5px solid #2e7d32; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

st.title("🩺 WEB SL 智能选型助手")
st.markdown("优先根据动脉瘤直径高度匹配，无匹配则自动体积测算")

# ================= 1. 数据定义 =================
# 表1：常规区间 (仅做初步索引)
H_RANGES = [(2.6, 3.6), (3.7, 4.9), (5.0, 5.9), (6.0, 6.9), (7.0, 7.9), (8.0, 8.9), (9.0, 9.9), (10.0, 10.9)]
W_RANGES = [(3.0, 3.4), (3.5, 3.8), (3.9, 4.3), (4.4, 5.0), (5.1, 6.0), (6.1, 7.0), (7.1, 8.0), (8.1, 9.0), (9.1, 10.0)]
DATA_MATRIX = [
    [("WEB SL 4x2", "VIA 17"), ("WEB SL 4.5x2", "VIA 17"), ("WEB SL 5x2", "VIA 17"), ("WEB SL 6x2", "VIA 17"), ("WEB SL 7x2", "VIA 17"), None, None, None, None],
    [("WEB SL 4x3", "VIA 17"), ("WEB SL 4.5x3", "VIA 17"), ("WEB SL 5x3", "VIA 17"), ("WEB SL 6x3", "VIA 17"), ("WEB SL 7x3", "VIA 17"), ("WEB SL 8x3", "VIA 27"), None, None, None],
    [None, None, None, ("WEB SL 6x4", "VIA 17"), ("WEB SL 7x4", "VIA 17"), ("WEB SL 8x4", "VIA 27"), ("WEB SL 9x4", "VIA 27"), None, None],
    [None, None, None, None, ("WEB SL 7x5", "VIA 17"), ("WEB SL 8x5", "VIA 27"), ("WEB SL 9x5", "VIA 27"), ("WEB SL 10x5", "VIA 33"), None],
    [None, None, None, None, None, ("WEB SL 8x6", "VIA 27"), ("WEB SL 9x6", "VIA 27"), ("WEB SL 10x6", "VIA 33"), ("WEB SL 11x6", "VIA 33")],
    [None, None, None, None, None, None, ("WEB SL 9x7", "VIA 27"), ("WEB SL 10x7", "VIA 33"), ("WEB SL 11x7", "VIA 33")],
    [None, None, None, None, None, None, None, ("WEB SL 10x8", "VIA 33"), ("WEB SL 11x8", "VIA 33")],
    [None, None, None, None, None, None, None, None, ("WEB SL 11x9", "VIA 33")]
]

# 表2：全WEB SL产品库 (用于查参数和体积验证)
# 转换为字典方便通过型号名称快速查找参数
ALL_PRODUCTS = {
    "WEB SL 4x2": {"d": 4, "h": 2, "v": 25.13, "c": "VIA 17"}, "WEB SL 4x3": {"d": 4, "h": 3, "v": 37.70, "c": "VIA 17"},
    "WEB SL 4.5x2": {"d": 4.5, "h": 2, "v": 31.81, "c": "VIA 17"}, "WEB SL 4.5x3": {"d": 4.5, "h": 3, "v": 47.71, "c": "VIA 17"},
    "WEB SL 5x2": {"d": 5, "h": 2, "v": 39.21, "c": "VIA 17"}, "WEB SL 5x3": {"d": 5, "h": 3, "v": 58.91, "c": "VIA 17"},
    "WEB SL 6x2": {"d": 6, "h": 2, "v": 56.55, "c": "VIA 17"}, "WEB SL 6x3": {"d": 6, "h": 3, "v": 84.82, "c": "VIA 17"},
    "WEB SL 6x4": {"d": 6, "h": 4, "v": 113.10, "c": "VIA 17"}, "WEB SL 7x2": {"d": 7, "h": 2, "v": 76.97, "c": "VIA 17"},
    "WEB SL 7x3": {"d": 7, "h": 3, "v": 115.45, "c": "VIA 17"}, "WEB SL 7x4": {"d": 7, "h": 4, "v": 153.94, "c": "VIA 17"},
    "WEB SL 7x5": {"d": 7, "h": 5, "v": 192.42, "c": "VIA 17"}, "WEB SL 8x3": {"d": 8, "h": 3, "v": 150.80, "c": "VIA 27"},
    "WEB SL 8x4": {"d": 8, "h": 4, "v": 201.06, "c": "VIA 27"}, "WEB SL 8x5": {"d": 8, "h": 5, "v": 251.33, "c": "VIA 27"},
    "WEB SL 8x6": {"d": 8, "h": 6, "v": 301.60, "c": "VIA 27"}, "WEB SL 9x4": {"d": 9, "h": 4, "v": 254.47, "c": "VIA 27"},
    "WEB SL 9x5": {"d": 9, "h": 5, "v": 318.09, "c": "VIA 27"}, "WEB SL 9x6": {"d": 9, "h": 6, "v": 381.70, "c": "VIA 27"},
    "WEB SL 9x7": {"d": 9, "h": 7, "v": 445.32, "c": "VIA 27"}, "WEB SL 10x5": {"d": 10, "h": 5, "v": 392.70, "c": "VIA 33"},
    "WEB SL 10x6": {"d": 10, "h": 6, "v": 471.24, "c": "VIA 33"}, "WEB SL 10x7": {"d": 10, "h": 7, "v": 549.78, "c": "VIA 33"},
    "WEB SL 10x8": {"d": 10, "h": 8, "v": 628.32, "c": "VIA 33"}, "WEB SL 11x6": {"d": 11, "h": 6, "v": 570.20, "c": "VIA 33"},
    "WEB SL 11x7": {"d": 11, "h": 7, "v": 665.23, "c": "VIA 33"}, "WEB SL 11x8": {"d": 11, "h": 8, "v": 760.27, "c": "VIA 33"},
    "WEB SL 11x9": {"d": 11, "h": 9, "v": 855.30, "c": "VIA 33"}
}

# ================= 2. 界面输入 =================
st.subheader("📝 请输入测量数据 (mm)")
col1, col2 = st.columns(2)
with col1:
    w1 = st.number_input("宽径1 (W1)", min_value=0.0, max_value=20.0, value=8.5, step=0.1)
    h = st.number_input("动脉瘤高度 (H)", min_value=0.0, max_value=20.0, value=6.5, step=0.1)
with col2:
    w2 = st.number_input("宽径2 (正交, W2)", min_value=0.0, max_value=20.0, value=8.5, step=0.1)
    neck = st.number_input("瘤颈宽度 (Neck)", min_value=0.0, max_value=20.0, value=3.5, step=0.1)

# ================= 3. 核心算法 =================
def find_fallback_model(w_avg, h, aneurysm_vol):
    """
    兜底寻找算法：
    硬性条件：直径 D >= 平均宽度 + 1.0; 高度 H_device <= 瘤高 - 1.0; 体积 V_device <= 瘤体积
    """
    candidates = []
    for name, p in ALL_PRODUCTS.items():
        # 1. 直径大于动脉瘤直径1mm (>= W_avg + 1.0)
        if p['d'] < (w_avg + 1.0):
            continue
        # 2. 高度低于动脉瘤高度1mm (<= H - 1.0)
        if p['h'] > (h - 1.0):
            continue
        # 3. 体积偏小 (<= 瘤体积)
        if p['v'] > aneurysm_vol:
            continue
        
        # 计算差值
        diff = aneurysm_vol - p['v']
        candidates.append((diff, name, p))
        
    # 按差值升序排列 (差值越小越接近)
    candidates.sort(key=lambda x: x[0])
    if candidates:
        return candidates[0][1], candidates[0][2]
    return None, None

if st.button("🔍 智能匹配型号", use_container_width=True, type="primary"):
    w_avg = round((w1 + w2) / 2, 2)
    aneurysm_vol = round((math.pi / 6) * (w_avg ** 2) * h, 2)
    
    st.markdown(f"**平均宽度：** {w_avg} mm | **动脉瘤估算体积：** {aneurysm_vol} mm³")
    st.markdown("---")
    
    # ================= 步骤 1：查表 1 =================
    w_idx = next((i for i, (min_w, max_w) in enumerate(W_RANGES) if min_w <= w_avg <= max_w), -1)
    h_idx = next((i for i, (min_h, max_h) in enumerate(H_RANGES) if min_h <= h <= max_h), -1)
    
    table1_name = None
    if w_idx != -1 and h_idx != -1:
        res = DATA_MATRIX[h_idx][w_idx]
        if res:
            table1_name, catheter = res
            
    # ================= 步骤 2：判断与验证 =================
    final_model_name = None
    final_catheter = None
    status_type = "" # 'table1_pass', 'table1_fail_vol', 'no_table1'
    
    if table1_name:
        # 表1查到了型号，用表2体积验证
        t1_p = ALL_PRODUCTS[table1_name]
        if t1_p['v'] <= aneurysm_vol:
            # 验证通过
            final_model_name = table1_name
            final_catheter = t1_p['c']
            status_type = 'table1_pass'
        else:
            # 验证不通过（体积偏大）
            status_type = 'table1_fail_vol'
    else:
        # 表1无匹配
        status_type = 'no_table1'

    # ================= 步骤 3：结果输出 =================
    if status_type == 'table1_pass':
        p = ALL_PRODUCTS[final_model_name]
        st.success(f"✅ **【表1 匹配且体积验证通过】**")
        col1, col2 = st.columns(2)
        col1.metric("推荐规格", final_model_name)
        col2.metric("匹配导管", final_catheter)
        st.markdown(f"""<div class="pass-box">
        <b>📐 体积验证：</b> 装置体积({p['v']} mm³) \(\le\) 动脉瘤体积({aneurysm_vol} mm³)。<br>
        <b>📏 装置尺寸：</b> 直径 {p['d']}mm × 高度 {p['h']}mm。
        </div>""", unsafe_allow_html=True)
        
    else:
        # 触发兜底
        if status_type == 'table1_fail_vol':
            t1_p = ALL_PRODUCTS[table1_name]
            st.warning(f"⚠️ **表1选出的【{table1_name}】体积({t1_p['v']} mm³)大于动脉瘤体积({aneurysm_vol} mm³)，验证不通过，已启动表2兜底选型。**")
        else:
            st.warning(f"⚠️ **表1无匹配区间，已启动表2体积测算兜底选型。**")
            
        st.markdown(f"**兜底条件：** 直径 \(\ge {w_avg + 1.0:.1f}\)mm (宽+1), 高度 \(\le {h - 1.0:.1f}\)mm (高-1), 体积偏小且最接近。")
        
        # 寻找兜底
        fallback_name, fallback_p = find_fallback_model(w_avg, h, aneurysm_vol)
        
        if fallback_name:
            st.success(f"✅ **【表2 兜底测算成功】**")
            col1, col2 = st.columns(2)
            col1.metric("推荐规格", fallback_name)
            col2.metric("匹配导管", fallback_p['c'])
            
            vol_diff = round(fallback_p['v'] - aneurysm_vol, 2)
            h_diff = round(h - fallback_p['h'], 2)
            d_diff = round(fallback_p['d'] - w_avg, 2)
            
            st.markdown(f"""<div class="vol-box">
            <b>📏 装置尺寸：</b> 直径 {fallback_p['d']}mm (比宽大{d_diff}mm) × 高度 {fallback_p['h']}mm (比高小{h_diff}mm)。<br>
            <b>📐 体积差：</b> 装置体积({fallback_p['v']} mm³) 比瘤体积小 {abs(vol_diff)} mm³。
            </div>""", unsafe_allow_html=True)
        else:
            st.error("❌ **【无法匹配】**：在兜底条件（直径宽1mm，高度低1mm，体积偏小）下，产品库中无合适型号。")
            st.markdown("建议：考虑其他治疗方式或人工放宽限制。")

    if neck > w_avg * 0.8:
        st.markdown(f"""<div class="warning-box">
        <b>💡 临床提示：</b> 瘤颈宽度 ({neck} mm) 相对偏宽。请评估植入后稳定性及是否需要辅助支架。
        </div>""", unsafe_allow_html=True)

st.caption("免责声明：本工具仅作为手术规划参考。最终选型必须由专业医师综合判断。")
