import streamlit as st
import math

st.set_page_config(page_title="WEB SL 智能选型助手", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; color: #2e7d32; }
    .warning-box { background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 5px solid #ffc107; margin-bottom: 20px;}
    .vol-box { background-color: #e3f2fd; padding: 15px; border-radius: 5px; border-left: 5px solid #1976d2; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

st.title("🩺 WEB SL 智能选型助手")
st.markdown("优先根据动脉瘤直径高度匹配，无匹配则自动体积测算")

# ================= 1. 数据定义 =================
# 表1：常规区间
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

# 表2：全WEB SL产品库
ALL_PRODUCTS = [
    {"name": "WEB SL 4x2", "d": 4, "h": 2, "v": 25.13, "c": "VIA 17"},
    {"name": "WEB SL 4x3", "d": 4, "h": 3, "v": 37.70, "c": "VIA 17"},
    {"name": "WEB SL 4.5x2", "d": 4.5, "h": 2, "v": 31.81, "c": "VIA 17"},
    {"name": "WEB SL 4.5x3", "d": 4.5, "h": 3, "v": 47.71, "c": "VIA 17"},
    {"name": "WEB SL 5x2", "d": 5, "h": 2, "v": 39.21, "c": "VIA 17"},
    {"name": "WEB SL 5x3", "d": 5, "h": 3, "v": 58.91, "c": "VIA 17"},
    {"name": "WEB SL 6x2", "d": 6, "h": 2, "v": 56.55, "c": "VIA 17"},
    {"name": "WEB SL 6x3", "d": 6, "h": 3, "v": 84.82, "c": "VIA 17"},
    {"name": "WEB SL 6x4", "d": 6, "h": 4, "v": 113.10, "c": "VIA 17"},
    {"name": "WEB SL 7x2", "d": 7, "h": 2, "v": 76.97, "c": "VIA 17"},
    {"name": "WEB SL 7x3", "d": 7, "h": 3, "v": 115.45, "c": "VIA 17"},
    {"name": "WEB SL 7x4", "d": 7, "h": 4, "v": 153.94, "c": "VIA 17"},
    {"name": "WEB SL 7x5", "d": 7, "h": 5, "v": 192.42, "c": "VIA 17"},
    {"name": "WEB SL 8x3", "d": 8, "h": 3, "v": 150.80, "c": "VIA 27"},
    {"name": "WEB SL 8x4", "d": 8, "h": 4, "v": 201.06, "c": "VIA 27"},
    {"name": "WEB SL 8x5", "d": 8, "h": 5, "v": 251.33, "c": "VIA 27"},
    {"name": "WEB SL 8x6", "d": 8, "h": 6, "v": 301.60, "c": "VIA 27"},
    {"name": "WEB SL 9x4", "d": 9, "h": 4, "v": 254.47, "c": "VIA 27"},
    {"name": "WEB SL 9x5", "d": 9, "h": 5, "v": 318.09, "c": "VIA 27"},
    {"name": "WEB SL 9x6", "d": 9, "h": 6, "v": 381.70, "c": "VIA 27"},
    {"name": "WEB SL 9x7", "d": 9, "h": 7, "v": 445.32, "c": "VIA 27"},
    {"name": "WEB SL 10x5", "d": 10, "h": 5, "v": 392.70, "c": "VIA 33"},
    {"name": "WEB SL 10x6", "d": 10, "h": 6, "v": 471.24, "c": "VIA 33"},
    {"name": "WEB SL 10x7", "d": 10, "h": 7, "v": 549.78, "c": "VIA 33"},
    {"name": "WEB SL 10x8", "d": 10, "h": 8, "v": 628.32, "c": "VIA 33"},
    {"name": "WEB SL 11x6", "d": 11, "h": 6, "v": 570.20, "c": "VIA 33"},
    {"name": "WEB SL 11x7", "d": 11, "h": 7, "v": 665.23, "c": "VIA 33"},
    {"name": "WEB SL 11x8", "d": 11, "h": 8, "v": 760.27, "c": "VIA 33"},
    {"name": "WEB SL 11x9", "d": 11, "h": 9, "v": 855.30, "c": "VIA 33"}
]

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
def get_volume_match(w_avg, h, aneurysm_vol):
    """
    体积匹配算法：
    1. 装置直径 D >= 平均宽度
    2. 装置高度 H_device <= 动脉瘤高度 H - 1.0 (必须短至少1mm)
    3. 装置体积 V_device <= 动脉瘤体积 V_aneurysm (偏小)
    """
    candidates = []
    min_h_allowed = h - 1.0 # 高度必须 <= H - 1.0
    
    for p in ALL_PRODUCTS:
        # 条件1：直径必须足够
        if p['d'] < w_avg:
            continue
            
        # 条件2：高度必须比瘤高小1mm及以上
        # 使用 round 避免浮点数精度问题
        if round(p['h'], 2) > round(min_h_allowed, 2):
            continue
            
        # 条件3：体积不能超过动脉瘤体积
        if round(p['v'], 2) > round(aneurysm_vol, 2):
            continue
            
        # 记录体积差值 (目标体积 - 装置体积)
        diff = aneurysm_vol - p['v']
        candidates.append((diff, p))
    
    # 按差值升序排序（差值越小，越接近理想体积）
    candidates.sort(key=lambda x: x[0])
    
    if candidates:
        return candidates[0][1], "符合所有限制 (D≥宽, H≤瘤高-1, V≤瘤体积) + 体积最饱满"
        
    return None, "在严格限制下（高度短1mm且体积不超标），无合适型号"

if st.button("🔍 智能匹配型号", use_container_width=True, type="primary"):
    w_avg = round((w1 + w2) / 2, 2)
    st.markdown(f"**平均动脉瘤宽度：{w_avg} mm**")
    st.markdown("---")
    
    # 1. 尝试表1匹配
    w_idx = next((i for i, (min_w, max_w) in enumerate(W_RANGES) if min_w <= w_avg <= max_w), -1)
    h_idx = next((i for i, (min_h, max_h) in enumerate(H_RANGES) if min_h <= h <= max_h), -1)
    
    table1_result = None
    if w_idx != -1 and h_idx != -1:
        table1_result = DATA_MATRIX[h_idx][w_idx]
        
    # 2. 结果判定
    if table1_result:
        # 表1匹配成功
        model, catheter = table1_result
        st.success(f"✅ **【表1 标准查表成功】**\n\n### 推荐规格：{model}\n### 匹配导管：{catheter}")
    else:
        # 表1无匹配，启动表2
        st.warning("⚠️ **常规二维表（表1）无匹配区间，已自动启用体积测算选型（表2）**")
        
        aneurysm_vol = round((math.pi / 6) * (w_avg ** 2) * h, 2)
        st.markdown(f"""<div class="vol-box">
        <b>📐 动脉瘤估算体积：</b> {aneurysm_vol} mm³ <br>
        <small>(采用公式: π/6 * 宽² * 高 估算)</small>
        </div>""", unsafe_allow_html=True)
        
        best_match, match_reason = get_volume_match(w_avg, h, aneurysm_vol)
        
        if best_match:
            st.info(f"💡 **匹配依据：** {match_reason}")
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("推荐规格", best_match['name'])
            col_r2.metric("匹配导管", best_match['c'])
            
            # 显示体积差额（必须是负数或0，表示偏小）
            vol_diff = round(best_match['v'] - aneurysm_vol, 2)
            col_r3.metric("装置体积", f"{best_match['v']} mm³", delta=f"{vol_diff} (偏小)", delta_color="inverse")
            
            h_diff = round(h - best_match['h'], 2)
            st.markdown(f"**装置尺寸：** 直径 {best_match['d']} mm × 高度 {best_match['h']} mm （比瘤高短 {h_diff} mm）")
        else:
            st.error("❌ **无法匹配：** 在“高度短于1mm且体积不超标”的严格限制下，无合适型号。")
            st.markdown("""
            **建议：**
            1. 可能是动脉瘤体积过小，导致现有装置最小的体积也超过了测算体积。
            2. 可能是高度限制严苛（如瘤高仅2.5mm，要求装置高度<=1.5mm，但最小装置高2mm）。
            3. 请结合临床实际情况，考虑其他治疗方式或人工放宽条件重新评估。
            """)

    # 临床提示
    if neck > w_avg * 0.8:
        st.markdown(f"""<div class="warning-box">
        <b>💡 临床提示：</b> 输入瘤颈宽度为 <b>{neck} mm</b>，相对偏宽。请评估植入后稳定性及是否需要辅助支架。
        </div>""", unsafe_allow_html=True)

st.caption("免责声明：本工具仅作为术者手术规划时的数据参考辅助。最终产品的选择及手术操作必须由具备资质的专业医师综合判断。")
