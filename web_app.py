import streamlit as st
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="محاكاة الأخلاقيات في الحرب الذكية",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيقات CSS مخصصة
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    .scenario-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        background-color: #f8f9fa;
        margin: 10px 0;
    }
    .decision-card {
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .decision-card:hover {
        border-color: #667eea;
        background-color: #f0f2f6;
    }
    .ethical-score {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #28a745;
    }
    .progress-bar {
        height: 20px;
        border-radius: 10px;
        background-color: #e9ecef;
        margin: 10px 0;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #28a745, #20c997);
    }
    .analysis-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #f8f9fa;
        border-left: 4px solid #6c757d;
    }
    .law-violation {
        border-left-color: #dc3545;
        background-color: #f8d7da;
    }
    .law-compliant {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .law-warning {
        border-left-color: #ffc107;
        background-color: #fff3cd;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# بيانات السيناريوهات - 10 سيناريوهات مختلفة
SCENARIOS = {
    1: {
        "id": 1,
        "title": "🚀 مستودع أسلحة في صحراء",
        "description": "مستودع أسلحة مؤكد بالصور الجوية في منطقة صحراوية غير مأهولة بالسكان",
        "difficulty": "🟢 سهل",
        "details": {
            "المكان": "صحراء غير مأهولة",
            "الهدف": "مستودع أسلحة ومعدات عسكرية",
            "المصادر": "صور أقمار صناعية + إشارات استخباراتية",
            "الوقت": "ليل",
            "القوانين المنطبقة": "قانون النزاعات المسلحة، مبدأ التمييز"
        },
        "metrics": {
            "التأكد": 95,
            "الخطر_المدني": 5,
            "القيمة_العسكرية": 90,
            "ضغط_الوقت": 20,
            "الضرورة": 85,
            "التناسب": 95
        },
        "image": "🏜️",
        "category": "أهداف تقليدية"
    },
    2: {
        "id": 2,
        "title": "🏢 مقر عسكري في مدينة",
        "description": "مقر قيادة عسكرية في الطابق الثالث من مبنى سكني في منطقة حضرية",
        "difficulty": "🟡 متوسط",
        "details": {
            "المكان": "حي سكني مكتظ",
            "الهدف": "مقر قيادة عسكري",
            "المصادر": "عميل مزدوج + مراقبة لاسلكية",
            "الوقت": "ظهر",
            "القوانين المنطبقة": "اتفاقية جنيف الرابعة، البروتوكول الإضافي الأول"
        },
        "metrics": {
            "التأكد": 70,
            "الخطر_المدني": 60,
            "القيمة_العسكرية": 80,
            "ضغط_الوقت": 50,
            "الضرورة": 75,
            "التناسب": 40
        },
        "image": "🏙️",
        "category": "أهداف مختلطة"
    },
    3: {
        "id": 3,
        "title": "🏫 مدرسة مشتبه بها",
        "description": "مدرسة يُشتبه في استخدامها كمقر لإطلاق صواريخ وكمستودع أسلحة",
        "difficulty": "🔴 صعب",
        "details": {
            "المكان": "مدرسة في منطقة سكنية",
            "الهدف": "مقر إطلاق صواريخ مشتبه به",
            "المصادر": "تقارير استخباراتية غير مؤكدة",
            "الوقت": "صباح",
            "القوانين المنطبقة": "حماية الممتلكات المدنية، القانون الدولي الإنساني"
        },
        "metrics": {
            "التأكد": 40,
            "الخطر_المدني": 85,
            "القيمة_العسكرية": 70,
            "ضغط_الوقت": 30,
            "الضرورة": 60,
            "التناسب": 20
        },
        "image": "📚",
        "category": "أهداف محمية"
    },
    4: {
        "id": 4,
        "title": "🚗 سيارة مفخخة متحركة",
        "description": "سيارة مفخخة تتحرك بسرعة نحو منطقة سكنية مكتظة، تحتوي على متفجرات",
        "difficulty": "🔴 صعب جداً",
        "details": {
            "المكان": "طريق سريع باتجاه مدينة",
            "الهدف": "سيارة مفخخة متحركة",
            "المصادر": "تنصت لاسلكي + مراقبة جوية",
            "الوقت": "عاجل (دقائق)",
            "القوانين المنطبقة": "الدفاع عن النفس، حالة الضرورة القصوى"
        },
        "metrics": {
            "التأكد": 85,
            "الخطر_المدني": 95,
            "القيمة_العسكرية": 99,
            "ضغط_الوقت": 95,
            "الضرورة": 98,
            "التناسب": 30
        },
        "image": "💥",
        "category": "تهديدات عاجلة"
    },
    5: {
        "id": 5,
        "title": "⚡ محطة طاقة مزدوجة الاستخدام",
        "description": "محطة طاقة تعمل على تشغيل منشأة عسكرية ولكنها أيضاً تزود مستشفى قريب",
        "difficulty": "🟡 متوسط",
        "details": {
            "المكان": "منطقة صناعية بالقرب من مستشفى",
            "الهدف": "محطة طاقة استراتيجية",
            "المصادر": "صور جوية + وثائق استخباراتية",
            "الوقت": "مساء",
            "القوانين المنطبقة": "مبدأ التناسب، حماية الخدمات الأساسية"
        },
        "metrics": {
            "التأكد": 80,
            "الخطر_المدني": 70,
            "القيمة_العسكرية": 85,
            "ضغط_الوقت": 40,
            "الضرورة": 65,
            "التناسب": 35
        },
        "image": "🏭",
        "category": "أهداف مزدوجة"
    },
    6: {
        "id": 6,
        "title": "🏥 مستشفى تحت الحصار",
        "description": "مستشفى يستخدمه مقاتلون كموقع لإطلاق الصواريخ، مع وجود مرضى وجرحى داخله",
        "difficulty": "🔴 صعب جداً",
        "details": {
            "المكان": "مستشفى مدني كبير",
            "الهدف": "مقاتلون داخل مستشفى",
            "المصادر": "معلومات استخباراتية + مشاهدات محلية",
            "الوقت": "نهار",
            "القوانين المنطبقة": "حماية الوحدات الطبية، القواعد الخاصة"
        },
        "metrics": {
            "التأكد": 75,
            "الخطر_المدني": 90,
            "القيمة_العسكرية": 60,
            "ضغط_الوقت": 60,
            "الضرورة": 50,
            "التناسب": 15
        },
        "image": "🚑",
        "category": "أهداف محمية دولياً"
    },
    7: {
        "id": 7,
        "title": "📡 مركز اتصالات مشترك",
        "description": "برج اتصالات يستخدم للاتصالات المدنية والعسكرية على حد سواء",
        "difficulty": "🟡 متوسط",
        "details": {
            "المكان": "قمة جبل بعيد عن السكان",
            "الهدف": "برج اتصالات استراتيجي",
            "المصادر": "اعتراض اتصالات + تحليل إشارات",
            "الوقت": "فجر",
            "القوانين المنطبقة": "قواعد الاستهداف، حماية البنى التحتية"
        },
        "metrics": {
            "التأكد": 90,
            "الخطر_المدني": 25,
            "القيمة_العسكرية": 75,
            "ضغط_الوقت": 35,
            "الضرورة": 70,
            "التناسب": 70
        },
        "image": "📶",
        "category": "أهداف استراتيجية"
    },
    8: {
        "id": 8,
        "title": "🚁 مروحية تهرب بجرحى",
        "description": "مروحية عسكرية تحمل جرحى ولكنها أيضاً تنقل قادة عسكريين مهمين",
        "difficulty": "🟠 صعب",
        "details": {
            "المكان": "مجال جوي فوق مناطق صحراوية",
            "الهدف": "مروحية عسكرية مختلطة",
            "المصادر": "رادار + مراقبة جوية",
            "الوقت": "ليل",
            "القوانين المنطبقة": "حماية الجرحى، قواعد الاشتباك الجوية"
        },
        "metrics": {
            "التأكد": 88,
            "الخطر_المدني": 15,
            "القيمة_العسكرية": 65,
            "ضغط_الوقت": 70,
            "الضرورة": 55,
            "التناسب": 60
        },
        "image": "🚁",
        "category": "أهداف متحركة"
    },
    9: {
        "id": 9,
        "title": "🏭 مصنع أسلحة تحت الأرض",
        "description": "مصنع لإنتاج الأسلحة الكيميائية مخبأ تحت الأرض بالقرب من منطقة سكنية",
        "difficulty": "🟡 متوسط",
        "details": {
            "المكان": "منطقة صناعية تحت الأرض",
            "الهدف": "مصنع أسلحة محظورة",
            "المصادر": "صور حرارية + معلومات من الهاربين",
            "الوقت": "منتصف الليل",
            "القوانين المنطبقة": "حظر الأسلحة الكيميائية، القانون الدولي"
        },
        "metrics": {
            "التأكد": 82,
            "الخطر_المدني": 55,
            "القيمة_العسكرية": 92,
            "ضغط_الوقت": 45,
            "الضرورة": 88,
            "التناسب": 50
        },
        "image": "⚠️",
        "category": "أسلحة محظورة"
    },
    10: {
        "id": 10,
        "title": "🎯 قيادي في حفل زفاف",
        "description": "قيادي عسكري رفيع المستوى يحضر حفل زفاف في فندق مع عائلته ومدنيين آخرين",
        "difficulty": "🔴 صعب جداً",
        "details": {
            "المكان": "فندق فاخر في وسط المدينة",
            "الهدف": "قيادي عسكري مهم",
            "المصادر": "مصدر استخباراتي سري",
            "الوقت": "مساء (خلال الاحتفال)",
            "القوانين المنطبقة": "مبدأ التمييز، حماية التجمعات المدنية"
        },
        "metrics": {
            "التأكد": 95,
            "الخطر_المدني": 88,
            "القيمة_العسكرية": 85,
            "ضغط_الوقت": 80,
            "الضرورة": 40,
            "التناسب": 10
        },
        "image": "💒",
        "category": "أهداف بشرية"
    }
}

# قرارات ممكنة
DECISIONS = [
    {"id": 1, "icon": "⚡", "title": "ضربة فورية", "description": "تنفيذ الهجوم فوراً دون تردد"},
    {"id": 2, "icon": "🔍", "title": "استطلاع إضافي", "description": "طلب معلومات وتأكيدات قبل القرار"},
    {"id": 3, "icon": "🤖", "title": "تفويض الذكاء الاصطناعي", "description": "ترك القرار للخوارزمية حسب معطياتها"},
    {"id": 4, "icon": "❌", "title": "رفض الضربة", "description": "إلغاء الهجوم والبحث عن بدائل"},
    {"id": 5, "icon": "🎯", "title": "ضربة جراحية", "description": "هجوم محدود بدقة عالية وتوقيت محدد"},
    {"id": 6, "icon": "🕵️", "title": "عملية خاصة", "description": "إرسال قوات خاصة للتعامل مع الهدف"}
]

# قواعد القانون الدولي الإنساني
INTERNATIONAL_LAWS = {
    "مبدأ التمييز": {
        "description": "التمييز بين الأهداف العسكرية والأشخاص المدنيين والممتلكات المدنية",
        "weight": 25,
        "threshold": 70
    },
    "مبدأ التناسب": {
        "description": "الخسائر المدنية لا تتناسب مع المكسب العسكري الملموس المتوقع",
        "weight": 25,
        "threshold": 60
    },
    "مبدأ الاحتياط": {
        "description": "اتخاذ جميع الاحتياطات الممكنة لتجنب إصابة المدنيين",
        "weight": 20,
        "threshold": 75
    },
    "الضرورة العسكرية": {
        "description": "الهدف يحقق ميزة عسكرية محددة وواضحة",
        "weight": 15,
        "threshold": 50
    },
    "الإنسانية": {
        "description": "منع المعاناة غير الضرورية والقسوة غير المبررة",
        "weight": 15,
        "threshold": 65
    }
}

# دالة التحليل القانوني التفصيلي
def analyze_international_law(scenario, decision_id):
    """تحليل القرار بناءً على القانون الدولي الإنساني"""
    analysis = []
    total_score = 0
    max_score = 0
    
    metrics = scenario["metrics"]
    
    # تحليل كل مبدأ
    for law, details in INTERNATIONAL_LAWS.items():
        score = 100
        violations = []
        compliances = []
        
        if law == "مبدأ التمييز":
            if metrics["التأكد"] < details["threshold"]:
                score -= (details["threshold"] - metrics["التأكد"]) * 1.5
                violations.append(f"درجة التأكد ({metrics['التأكد']}%) أقل من الحد الأدنى ({details['threshold']}%)")
            if metrics["الخطر_المدني"] > 50:
                score -= 20
                violations.append("خطر مدني مرتفع يشير إلى صعوبة التمييز")
            else:
                compliances.append("الهدف واضح والمعطيات كافية للتمييز")
                
        elif law == "مبدأ التناسب":
            proportion_score = metrics["التناسب"]
            if proportion_score < details["threshold"]:
                score -= (details["threshold"] - proportion_score) * 2
                violations.append(f"معدل التناسب ({proportion_score}%) منخفض جداً")
            else:
                compliances.append(f"التناسب مقبول ({proportion_score}%)")
                
        elif law == "مبدأ الاحتياط":
            if decision_id == 1:  # ضربة فورية
                if metrics["ضغط_الوقت"] < 80:  # ليس حالة طارئة قصوى
                    score -= 30
                    violations.append("ضربة فورية دون استطلاع إضافي تنتهك مبدأ الاحتياط")
            elif decision_id == 2:  # استطلاع إضافي
                score += 15
                compliances.append("الاستطلاع الإضافي يتوافق مع الاحتياط الواجب")
                
        elif law == "الضرورة العسكرية":
            if metrics["الضرورة"] < details["threshold"]:
                score -= (details["threshold"] - metrics["الضرورة"]) * 1.2
                violations.append(f"الضرورة العسكرية ({metrics['الضرورة']}%) غير كافية")
            else:
                compliances.append(f"الضرورة العسكرية ({metrics['الضرورة']}%) مبررة")
                
        elif law == "الإنسانية":
            if decision_id in [1, 3] and metrics["الخطر_المدني"] > 70:
                score -= 35
                violations.append("خطر إصابات مدنية مرتفع يتعارض مع مبدأ الإنسانية")
            elif decision_id in [2, 4, 6]:
                score += 10
                compliances.append("القرار يأخذ بعين الاعتبار البعد الإنساني")
        
        # ضبط النتيجة النهائية
        score = max(0, min(100, score))
        law_score = (score / 100) * details["weight"]
        total_score += law_score
        max_score += details["weight"]
        
        # تصنيف مستوى الانتهاك
        if score < 50:
            status = "انتهاك جسيم"
            status_class = "law-violation"
        elif score < 70:
            status = "انتهاك طفيف"
            status_class = "law-warning"
        else:
            status = "مطابق"
            status_class = "law-compliant"
        
        analysis.append({
            "law": law,
            "score": score,
            "weight": details["weight"],
            "weighted_score": law_score,
            "status": status,
            "status_class": status_class,
            "violations": violations,
            "compliances": compliances,
            "description": details["description"]
        })
    
    # حساب النسبة المئوية الإجمالية
    overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    # التقييم العام
    if overall_percentage >= 80:
        overall_status = "مطابق للقانون الدولي"
        overall_class = "law-compliant"
    elif overall_percentage >= 60:
        overall_status = "مطابق جزئياً"
        overall_class = "law-warning"
    else:
        overall_status = "منتهك للقانون الدولي"
        overall_class = "law-violation"
    
    return {
        "detailed_analysis": analysis,
        "overall_score": round(overall_percentage, 1),
        "overall_status": overall_status,
        "overall_class": overall_class,
        "raw_score": total_score,
        "max_score": max_score
    }

# دالة التحليل الأخلاقي التفصيلي
def analyze_ethical_dimensions(scenario, decision_id):
    """تحليل الأبعاد الأخلاقية المختلفة للقرار"""
    dimensions = {
        "المسؤولية البشرية": {
            "weight": 20,
            "description": "درجة تحمل الإنسان للمسؤولية عن القرار",
            "analysis": ""
        },
        "الشفافية والمساءلة": {
            "weight": 15,
            "description": "القدرة على تبرير القرار وتحمل تبعاته",
            "analysis": ""
        },
        "العدالة والإنصاف": {
            "weight": 15,
            "description": "معاملة جميع الأطراف بعدالة وإنصاف",
            "analysis": ""
        },
        "السلامة والموثوقية": {
            "weight": 15,
            "description": "ضمان دقة النظام وموثوقيته",
            "analysis": ""
        },
        "الاستقلالية البشرية": {
            "weight": 15,
            "description": "حفظ حق الإنسان في اتخاذ القرارات المصيرية",
            "analysis": ""
        },
        "الكرامة الإنسانية": {
            "weight": 10,
            "description": "احترام كرامة جميع الأطراف المتأثرة",
            "analysis": ""
        },
        "المصلحة العامة": {
            "weight": 10,
            "description": "تحقيق أكبر فائدة لأكبر عدد من الناس",
            "analysis": ""
        }
    }
    
    metrics = scenario["metrics"]
    total_score = 0
    max_score = 0
    
    # تحليل كل بعد
    for dim, details in dimensions.items():
        score = 100
        
        if dim == "المسؤولية البشرية":
            if decision_id == 3:  # تفويض الذكاء الاصطناعي
                if metrics["الخطر_المدني"] > 30:
                    score -= 40
                    details["analysis"] = "تفويض قرارات خطيرة للذكاء الاصطناعي يضعف المسؤولية البشرية"
                else:
                    score -= 15
                    details["analysis"] = "تفويض محدود مع احتفاظ البشر بالسيطرة النهائية"
            else:
                score += 10
                details["analysis"] = "المسؤولية البشرية واضحة ومباشرة"
                
        elif dim == "الشفافية والمساءلة":
            if decision_id == 3:  # تفويض الذكاء الاصطناعي
                if metrics["التأكد"] < 90:
                    score -= 30
                    details["analysis"] = "صعوبة تبرير قرارات الذكاء الاصطناعي عند انخفاض التأكد"
                else:
                    score -= 10
                    details["analysis"] = "إمكانية التتبع والمراجعة متاحة"
            else:
                score += 5
                details["analysis"] = "القرار البشري يمكن تبريره ومراجعته"
                
        elif dim == "العدالة والإنصاف":
            if metrics["الخطر_المدني"] > 70 and decision_id in [1, 3]:
                score -= 35
                details["analysis"] = "تعريض المدنيين للخطر بشكل غير متناسب"
            elif decision_id == 5:  # ضربة جراحية
                score += 15
                details["analysis"] = "الضربة الجراحية تظهر اهتماماً بالعدالة والدقة"
            else:
                details["analysis"] = "القرار متوازن من حيث العدالة"
                
        elif dim == "السلامة والموثوقية":
            if metrics["التأكد"] < 70:
                score -= (70 - metrics["التأكد"])
                details["analysis"] = f"انخفاض درجة التأكد ({metrics['التأكد']}%) يؤثر على الموثوقية"
            else:
                details["analysis"] = "المعطيات موثوقة والقرار مبني على معلومات جيدة"
                
        elif dim == "الاستقلالية البشرية":
            if decision_id == 3 and metrics["القيمة_العسكرية"] > 80:
                score -= 25
                details["analysis"] = "تفويض قرارات مصيرية للآلة يؤثر على الاستقلالية البشرية"
            else:
                details["analysis"] = "السيطرة البشرية محفوظة بشكل مناسب"
                
        elif dim == "الكرامة الإنسانية":
            if metrics["الخطر_المدني"] > 50 and decision_id in [1, 3]:
                score -= 30
                details["analysis"] = "تعريض حياة المدنيين للخطر يمس بكرامتهم الإنسانية"
            else:
                details["analysis"] = "القرار يحترم الكرامة الإنسانية للمتأثرين"
                
        elif dim == "المصلحة العامة":
            if metrics["القيمة_العسكرية"] > 70 and decision_id != 4:
                score += metrics["الضرورة"] / 100 * 20
                details["analysis"] = "القرار يحقق مصلحة عسكرية عامة"
            elif decision_id == 4 and metrics["الخطر_المدني"] > 70:
                score += 20
                details["analysis"] = "حماية المدنيين تخدم المصلحة العامة الإنسانية"
            else:
                details["analysis"] = "تأثير متوازن على المصلحة العامة"
        
        score = max(0, min(100, score))
        weighted_score = (score / 100) * details["weight"]
        total_score += weighted_score
        max_score += details["weight"]
        details["score"] = score
        details["weighted_score"] = weighted_score
    
    overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    return {
        "dimensions": dimensions,
        "overall_score": round(overall_percentage, 1),
        "raw_score": total_score,
        "max_score": max_score
    }

# دالة التحليل العسكري العملياتي
def analyze_military_operational(scenario, decision_id):
    """تحليل الجوانب العسكرية والعملياتية"""
    metrics = scenario["metrics"]
    analysis_points = []
    score = 100
    
    # تحليل القيمة العسكرية
    if metrics["القيمة_العسكرية"] >= 90:
        analysis_points.append(("🎯 عالية جداً", "الهدف ذو قيمة استراتيجية كبرى"))
        if decision_id in [4, 2]:  # رفض أو تأخير
            score -= 25
    elif metrics["القيمة_العسكرية"] >= 70:
        analysis_points.append(("🎯 عالية", "الهدف مهم عملياتياً"))
    else:
        analysis_points.append(("🎯 متوسطة", "قيمة عسكرية محدودة"))
        if decision_id in [1, 3]:  # ضربة فورية أو تفويض
            score -= 15
    
    # تحليل الضرورة العسكرية
    if metrics["الضرورة"] >= 90:
        analysis_points.append(("⚡ قصوى", "ضرورة عسكرية ملحة"))
        if decision_id == 4:  # رفض
            score -= 40
    elif metrics["الضرورة"] >= 70:
        analysis_points.append(("⚡ عالية", "ضرورة عسكرية واضحة"))
    elif metrics["الضرورة"] >= 50:
        analysis_points.append(("⚡ متوسطة", "ضرورة عسكرية مقبولة"))
    else:
        analysis_points.append(("⚡ منخفضة", "ضرورة عسكرية مشكوك فيها"))
        if decision_id in [1, 3, 5]:  # أي نوع ضربة
            score -= 30
    
    # تحليل ضغط الوقت
    if metrics["ضغط_الوقت"] >= 90:
        analysis_points.append(("⏰ عاجل", "قرار عاجل خلال دقائق"))
        if decision_id in [2, 6]:  # استطلاع أو عملية خاصة
            score -= 35
    elif metrics["ضغط_الوقت"] >= 70:
        analysis_points.append(("⏰ مرتفع", "ضغط زمني كبير"))
    elif metrics["ضغط_الوقت"] >= 40:
        analysis_points.append(("⏰ متوسط", "وقت كافٍ للتخطيط"))
    else:
        analysis_points.append(("⏰ منخفض", "لا يوجد إلحاح زمني"))
        if decision_id == 1:  # ضربة فورية
            score -= 20
    
    # تحليل ملاءمة القرار
    decision_appropriateness = {
        1: "ضربة فورية مناسبة للتهديدات العاجلة فقط",
        2: "استطلاع إضافي ضروري عند انخفاض التأكد",
        3: "تفويض الذكاء الاصطناعي مناسب للأهداف الواضحة",
        4: "الرفض مناسب عندما تفوق المخاطر الفوائد",
        5: "الضربة الجراحية مثالية للأهداف الحساسة",
        6: "العملية الخاصة مناسبة للأهداف المعقدة"
    }
    
    analysis_points.append(("🤔 ملاءمة", decision_appropriateness.get(decision_id, "قرار غير معروف")))
    
    # تصحيح النتيجة
    score = max(0, min(100, score))
    
    return {
        "analysis_points": analysis_points,
        "score": round(score, 1),
        "recommendation": generate_military_recommendation(metrics, decision_id)
    }

def generate_military_recommendation(metrics, decision_id):
    """توليد توصية عسكرية بناءً على المعطيات"""
    recommendations = []
    
    # توصيات بناءً على القيمة العسكرية
    if metrics["القيمة_العسكرية"] >= 90:
        recommendations.append("الهدف عالي القيمة - يحتاج التعامل السريع")
    elif metrics["القيمة_العسكرية"] <= 40:
        recommendations.append("قيمة الهدف محدودة - مراجعة الجدوى")
    
    # توصيات بناءً على الخطر المدني
    if metrics["الخطر_المدني"] >= 80:
        recommendations.append("خطر مدني مرتفع جداً - تجنب الضربات التقليدية")
    elif metrics["الخطر_المدني"] >= 60:
        recommendations.append("خطر مدني مرتفع - النظر في بدائل")
    
    # توصيات بناءً على ضغط الوقت
    if metrics["ضغط_الوقت"] >= 90:
        recommendations.append("حالة طارئة - قرار سريع مطلوب")
    elif metrics["ضغط_الوقت"] <= 30:
        recommendations.append("وقت كافٍ للتخطيط الدقيق")
    
    # توصيات خاصة بالقرار
    if decision_id == 3 and metrics["التأكد"] < 85:
        recommendations.append("التفويض للذكاء الاصطناعي غير موصى به مع انخفاض التأكد")
    
    return recommendations

# دالة حساب النتيجة الإجمالية
def calculate_overall_score(scenario, decision_id, law_analysis, ethical_analysis, military_analysis):
    """حساب النتيجة الإجمالية الموزونة"""
    # الأوزان النسبية
    weights = {
        "legal": 40,      # القانون الدولي
        "ethical": 35,    # الأخلاقيات
        "military": 25    # الاعتبارات العسكرية
    }
    
    # استخراج النقاط
    legal_score = law_analysis["overall_score"]
    ethical_score = ethical_analysis["overall_score"]
    military_score = military_analysis["score"]
    
    # حساب النتيجة الموزونة
    weighted_score = (
        (legal_score * weights["legal"]) +
        (ethical_score * weights["ethical"]) +
        (military_score * weights["military"])
    ) / sum(weights.values())
    
    return round(weighted_score, 1)

# دالة للحصول على التقييم النهائي
def get_final_judgment(overall_score, law_analysis, ethical_analysis, military_analysis):
    """الحصول على التقييم النهائي مع التفسير"""
    
    if overall_score >= 90:
        judgment = "🎉 ممتاز - قرار نموذجي"
        color = "#28a745"
        explanation = "القرار يلتزم بالقانون الدولي، ويحترم المبادئ الأخلاقية، ويحقق الأهداف العسكرية بشكل متوازن."
    elif overall_score >= 80:
        judgment = "👍 جيد جداً - قرار مسؤول"
        color = "#20c997"
        explanation = "القرار جيد من النواحي القانونية والأخلاقية والعسكرية مع هامش تحسين طفيف."
    elif overall_score >= 70:
        judgment = "⚠️ مقبول - يحتاج تحسين"
        color = "#ffc107"
        explanation = "القرار مقبول ولكن هناك جوانب تحتاج مراجعة وتحسين."
    elif overall_score >= 60:
        judgment = "🔶 محفوف بالمخاطر"
        color = "#fd7e14"
        explanation = "القرار ينطوي على مخاطر قانونية أو أخلاقية أو عسكرية تحتاج تقييماً دقيقاً."
    elif overall_score >= 40:
        judgment = "⚠️ مشكوك في أخلاقيته"
        color = "#dc3545"
        explanation = "هناك مؤشرات قوية على انتهاكات قانونية أو أخلاقية محتملة."
    else:
        judgment = "❌ غير أخلاقي وغير قانوني"
        color = "#990000"
        explanation = "القرار ينتهك المبادئ الأساسية للقانون الدولي والأخلاقيات العسكرية."
    
    # تقرير تفصيلي
    detailed_report = []
    
    if law_analysis["overall_score"] < 60:
        detailed_report.append(f"📜 **مشاكل قانونية**: {law_analysis['overall_status']}")
    if ethical_analysis["overall_score"] < 60:
        detailed_report.append("⚖️ **مشاكل أخلاقية**: انخفاض في معايير الأخلاقيات")
    if military_analysis["score"] < 60:
        detailed_report.append("🎯 **مشاكل عسكرية**: عدم تحقيق الأهداف العملياتية بكفاءة")
    
    if not detailed_report:
        detailed_report.append("✅ لا توجد مشاكل رئيسية في القرار")
    
    return {
        "judgment": judgment,
        "color": color,
        "explanation": explanation,
        "detailed_report": detailed_report,
        "scores": {
            "legal": law_analysis["overall_score"],
            "ethical": ethical_analysis["overall_score"],
            "military": military_analysis["score"]
        }
    }
    # استمرارية الكود من الجزء الأول...

# الشريط الجانبي
with st.sidebar:
    st.markdown("### 🎯 اختيار السيناريو")
    
    # عرض السيناريوهات مصنفة حسب الصعوبة
    st.markdown("#### حسب الصعوبة:")
    
    # تصنيف السيناريوهات
    easy_scenarios = {k: v for k, v in SCENARIOS.items() if "🟢" in v["difficulty"]}
    medium_scenarios = {k: v for k, v in SCENARIOS.items() if "🟡" in v["difficulty"]}
    hard_scenarios = {k: v for k, v in SCENARIOS.items() if "🟠" in v["difficulty"]}
    very_hard_scenarios = {k: v for k, v in SCENARIOS.items() if "🔴" in v["difficulty"]}
    
    if easy_scenarios:
        st.markdown("**🟢 سهلة:**")
        for key, scenario in easy_scenarios.items():
            if st.button(f"{scenario['image']} {scenario['title'][:20]}...", key=f"btn_{key}"):
                st.session_state.selected_scenario = key
                st.rerun()
    
    if medium_scenarios:
        st.markdown("**🟡 متوسطة:**")
        for key, scenario in medium_scenarios.items():
            if st.button(f"{scenario['image']} {scenario['title'][:20]}...", key=f"btn_{key}_m"):
                st.session_state.selected_scenario = key
                st.rerun()
    
    if hard_scenarios:
        st.markdown("**🟠 صعبة:**")
        for key, scenario in hard_scenarios.items():
            if st.button(f"{scenario['image']} {scenario['title'][:20]}...", key=f"btn_{key}_h"):
                st.session_state.selected_scenario = key
                st.rerun()
    
    if very_hard_scenarios:
        st.markdown("**🔴 صعبة جداً:**")
        for key, scenario in very_hard_scenarios.items():
            if st.button(f"{scenario['image']} {scenario['title'][:20]}...", key=f"btn_{key}_vh"):
                st.session_state.selected_scenario = key
                st.rerun()
    
    st.markdown("---")
    
    # اختيار من قائمة
    selected_scenario = st.selectbox(
        "أو اختر من القائمة:",
        options=list(SCENARIOS.keys()),
        format_func=lambda x: f"{SCENARIOS[x]['title']}",
        key="scenario_selectbox"
    )
    
    st.markdown("---")
    st.markdown("### 📊 معايير التقييم")
    
    with st.expander("القانون الدولي الإنساني"):
        st.markdown("""
        1. **مبدأ التمييز**: التمييز بين العسكريين والمدنيين
        2. **مبدأ التناسب**: التوازن بين المكسب العسكري والخسائر المدنية
        3. **مبدأ الاحتياط**: اتخاذ كل الاحتياطات الممكنة
        4. **الضرورة العسكرية**: تحقيق ميزة عسكرية واضحة
        5. **مبدأ الإنسانية**: منع المعاناة غير الضرورية
        """)
    
    with st.expander("الأخلاقيات"):
        st.markdown("""
        1. **المسؤولية البشرية**: تحمل الإنسان للمسؤولية النهائية
        2. **الشفافية**: إمكانية تتبع ومراجعة القرارات
        3. **العدالة**: معاملة متساوية وعادلة
        4. **الكرامة الإنسانية**: احترام كرامة جميع البشر
        5. **الاستقلالية**: الحفاظ على السيطرة البشرية
        """)
    
    with st.expander("الاعتبارات العسكرية"):
        st.markdown("""
        1. **القيمة العسكرية**: أهمية الهدف استراتيجياً
        2. **الضرورة العملياتية**: الحاجة الملحة للعمل
        3. **التوقيت**: عامل الوقت والاستغلال الأمثل
        4. **البدائل المتاحة**: خيارات بديلة للعمل العسكري
        5. **العواقب**: التأثير طويل المدى للقرار
        """)
    
    st.markdown("---")
    st.markdown("### 📈 الإحصائيات")
    
    if 'decision_history' in st.session_state and st.session_state.decision_history:
        total_decisions = len(st.session_state.decision_history)
        avg_score = sum(d['overall_score'] for d in st.session_state.decision_history) / total_decisions
        st.metric("عدد القرارات", total_decisions)
        st.metric("متوسط النتيجة", f"{avg_score:.1f}/100")
    else:
        st.info("لم تتخذ أي قرارات بعد")

# تهيئة حالة الجلسة
if 'selected_scenario' not in st.session_state:
    st.session_state.selected_scenario = 1
if 'decision_history' not in st.session_state:
    st.session_state.decision_history = []

# العنوان الرئيسي
st.markdown("""
<div class="main-header">
    <h1>🎮 نظام محاكاة الأخلاقيات في الحرب الذكية</h1>
    <p>محاكاة تفاعلية لاتخاذ القرارات الأخلاقية والقانونية والعسكرية في استخدام الذكاء الاصطناعي</p>
</div>
""", unsafe_allow_html=True)

# استخدام السيناريو المحدد
selected_scenario = st.session_state.get('selected_scenario', selected_scenario)
scenario = SCENARIOS[selected_scenario]

# المحتوى الرئيسي
col1, col2 = st.columns([2, 1])

with col1:
    # عرض السيناريو
    st.markdown(f"## {scenario['image']} {scenario['title']}")
    st.markdown(f"**{scenario['description']}**")
    
    # تفاصيل السيناريو
    with st.expander("📋 تفاصيل السيناريو الكاملة", expanded=True):
        cols_details = st.columns(2)
        with cols_details[0]:
            for key, value in list(scenario["details"].items())[:3]:
                st.markdown(f"**{key}:** {value}")
        with cols_details[1]:
            for key, value in list(scenario["details"].items())[3:]:
                st.markdown(f"**{key}:** {value}")
    
    # المقاييس في أشرطة تقدم
    st.markdown("### 📊 مقاييس السيناريو الكمية")
    
    metrics_cols = st.columns(3)
    metrics = scenario["metrics"]
    
    metric_display = [
        ("التأكد", metrics["التأكد"], "درجة ثقة المعلومات والبيانات"),
        ("الخطر المدني", metrics["الخطر_المدني"], "احتمالية إصابة مدنيين"),
        ("القيمة العسكرية", metrics["القيمة_العسكرية"], "الأهمية الاستراتيجية للهدف"),
        ("ضغط الوقت", metrics["ضغط_الوقت"], "الإلحاح الزمني للقرار"),
        ("الضرورة", metrics["الضرورة"], "الضرورة العسكرية للعمل"),
        ("التناسب", metrics["التناسب"], "توازن الفائدة العسكرية مع الخسائر")
    ]
    
    for i, (name, value, desc) in enumerate(metric_display):
        with metrics_cols[i % 3]:
            st.markdown(f"**{name}**")
            st.markdown(f"`{value}%`")
            st.progress(value / 100)
            st.caption(desc)

with col2:
    st.markdown("### 🎯 اتخاذ القرار")
    
    # عرض القرارات مع وصف تفصيلي
    selected_decision = st.radio(
        "اختر قرارك:",
        options=[d["id"] for d in DECISIONS],
        format_func=lambda x: f"{DECISIONS[x-1]['icon']} {DECISIONS[x-1]['title']}",
        key="decision_radio_main"
    )
    
    # وصف مفصل للقرار المختار
    decision = DECISIONS[selected_decision - 1]
    
    with st.expander(f"📝 تفاصيل القرار: {decision['title']}", expanded=True):
        st.markdown(f"**الوصف:** {decision['description']}")
        
        # إضافة معلومات عن كل قرار
        decision_details = {
            1: "✅ **المزايا:** سرعة التنفيذ، منع هروب الهدف\n\n❌ **المخاطر:** أخطاء محتملة، خسائر مدنية",
            2: "✅ **المزايا:** زيادة الدقة، تقليل الأخطاء\n\n❌ **المخاطر:** فقدان الفرصة، تحذير الهدف",
            3: "✅ **المزايا:** سرعة المعالجة، تحييد العواطف\n\n❌ **المخاطر:** فقدان السيطرة البشرية، صعوبة المساءلة",
            4: "✅ **المزايا:** حماية المدنيين، تجنب الانتهاكات\n\n❌ **المخاطر:** استمرار التهديد، فرصة ضائعة",
            5: "✅ **المزايا:** دقة عالية، خسائر محدودة\n\n❌ **المخاطر:** تعقيد عملياتي، تكاليف عالية",
            6: "✅ **المزايا:** مرونة عالية، تجنب الضربات الجوية\n\n❌ **المخاطر:** مخاطر على القوات، وقت طويل"
        }
        
        st.markdown(decision_details.get(selected_decision, "لا توجد معلومات إضافية"))
    
    # زر اتخاذ القرار
    if st.button("🚀 اتخذ القرار وتحليل النتائج", type="primary", use_container_width=True):
        # إجراء التحليلات الثلاثة
        with st.spinner("🔍 جاري التحليل القانوني..."):
            law_analysis = analyze_international_law(scenario, selected_decision)
        
        with st.spinner("⚖️ جاري التحليل الأخلاقي..."):
            ethical_analysis = analyze_ethical_dimensions(scenario, selected_decision)
        
        with st.spinner("🎯 جاري التحليل العسكري..."):
            military_analysis = analyze_military_operational(scenario, selected_decision)
        
        # حساب النتيجة الإجمالية
        overall_score = calculate_overall_score(scenario, selected_decision, law_analysis, ethical_analysis, military_analysis)
        
        # الحصول على التقييم النهائي
        final_judgment = get_final_judgment(overall_score, law_analysis, ethical_analysis, military_analysis)
        
        # حفظ في سجل القرارات
        decision_record = {
            "scenario_id": scenario["id"],
            "scenario_title": scenario["title"],
            "decision_id": selected_decision,
            "decision_title": decision["title"],
            "overall_score": overall_score,
            "legal_score": law_analysis["overall_score"],
            "ethical_score": ethical_analysis["overall_score"],
            "military_score": military_analysis["score"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.decision_history.append(decision_record)
        
        # عرض النتائج في علامات تبويب
        st.markdown("---")
        st.markdown("## 📊 نتائج التحليل الشامل")
        
        # النتيجة الإجمالية
        st.markdown(f'<div class="ethical-score" style="color: {final_judgment["color"]};">{overall_score}/100</div>', unsafe_allow_html=True)
        st.markdown(f'### <span style="color: {final_judgment["color"]};">{final_judgment["judgment"]}</span>', unsafe_allow_html=True)
        st.info(final_judgment["explanation"])
        
        # علامات التبويب للتحليلات التفصيلية
        tab1, tab2, tab3, tab4 = st.tabs(["📜 التحليل القانوني", "⚖️ التحليل الأخلاقي", "🎯 التحليل العسكري", "📋 التقرير النهائي"])
        
        with tab1:
            st.markdown(f"### 📜 التحليل القانوني الدولي")
            st.markdown(f"**النتيجة الإجمالية:** {law_analysis['overall_score']}/100")
            st.markdown(f"**الحالة:** <span class='{law_analysis['overall_class']}'>{law_analysis['overall_status']}</span>", unsafe_allow_html=True)
            
            for item in law_analysis["detailed_analysis"]:
                with st.expander(f"{item['law']} - {item['status']} ({item['score']}/100)"):
                    st.markdown(f"**الوصف:** {item['description']}")
                    st.markdown(f"**الوزن:** {item['weight']}%")
                    st.markdown(f"**النتيجة الموزونة:** {item['weighted_score']:.1f}")
                    
                    if item['violations']:
                        st.markdown("**الانتهاكات:**")
                        for violation in item['violations']:
                            st.markdown(f"❌ {violation}")
                    
                    if item['compliances']:
                        st.markdown("**المطابقات:**")
                        for compliance in item['compliances']:
                            st.markdown(f"✅ {compliance}")
        
        with tab2:
            st.markdown(f"### ⚖️ التحليل الأخلاقي متعدد الأبعاد")
            st.markdown(f"**النتيجة الإجمالية:** {ethical_analysis['overall_score']}/100")
            
            # عرض الأبعاد الأخلاقية
            for dim_name, dim_data in ethical_analysis["dimensions"].items():
                score = dim_data["score"]
                color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
                
                col_dim1, col_dim2, col_dim3 = st.columns([2, 1, 3])
                with col_dim1:
                    st.markdown(f"**{dim_name}**")
                with col_dim2:
                    st.markdown(f"<span style='color: {color}; font-weight: bold;'>{score}/100</span>", unsafe_allow_html=True)
                with col_dim3:
                    st.caption(dim_data["analysis"])
        
        with tab3:
            st.markdown(f"### 🎯 التحليل العسكري والعملياتي")
            st.markdown(f"**النتيجة الإجمالية:** {military_analysis['score']}/100")
            
            st.markdown("#### نقاط التحليل:")
            for point, description in military_analysis['analysis_points']:
                st.markdown(f"- **{point}:** {description}")
            
            st.markdown("#### التوصيات العسكرية:")
            for recommendation in military_analysis['recommendation']:
                st.markdown(f"📍 {recommendation}")
        
        with tab4:
            st.markdown("### 📋 التقرير النهائي والتوصيات")
            
            # النتائج المقارنة
            st.markdown("#### 📈 النتائج المقارنة:")
            cols_scores = st.columns(3)
            with cols_scores[0]:
                st.metric("القانوني", f"{final_judgment['scores']['legal']}/100")
            with cols_scores[1]:
                st.metric("الأخلاقي", f"{final_judgment['scores']['ethical']}/100")
            with cols_scores[2]:
                st.metric("العسكري", f"{final_judgment['scores']['military']}/100")
            
            # التقرير التفصيلي
            st.markdown("#### 📝 ملخص التقييم:")
            for item in final_judgment['detailed_report']:
                st.markdown(f"- {item}")
            
            # التوصيات النهائية
            st.markdown("#### 💡 التوصيات:")
            
            recommendations = []
            
            # توصيات بناءً على النتائج
            if final_judgment['scores']['legal'] < 60:
                recommendations.append("🔴 **تعديل القرار** ليتوافق مع القانون الدولي الإنساني")
            elif final_judgment['scores']['legal'] < 80:
                recommendations.append("🟡 **مراجعة القرار** لتحسين التوافق القانوني")
            
            if final_judgment['scores']['ethical'] < 60:
                recommendations.append("🔴 **إعادة النظر** في الجوانب الأخلاقية للقرار")
            elif final_judgment['scores']['ethical'] < 80:
                recommendations.append("🟡 **تعزيز** البعد الأخلاقي في القرار")
            
            if final_judgment['scores']['military'] < 60:
                recommendations.append("🔴 **تحسين** الكفاءة العسكرية للقرار")
            elif final_judgment['scores']['military'] < 80:
                recommendations.append("🟡 **تحسين** التخطيط العملياتي")
            
            if overall_score >= 80:
                recommendations.append("✅ **تنفيذ القرار** كما هو")
            elif overall_score >= 70:
                recommendations.append("✅ **تنفيذ القرار** مع بعض التعديلات الطفيفة")
            elif overall_score >= 60:
                recommendations.append("⚠️ **التنفيذ بحذر** مع خطط طوارئ")
            else:
                recommendations.append("❌ **إلغاء القرار** والبحث عن بدائل")
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
            
            # درس مستفاد
            st.markdown("#### 🎓 الدرس المستفاد:")
            lessons = [
                "القرارات الأخلاقية تتطلب موازنة دقيقة بين المتطلبات العسكرية والالتزامات الإنسانية",
                "التفويض للذكاء الاصطناعي يجب أن يكون محدوداً ومشروطاً بالسيطرة البشرية",
                "الشفافية والمساءلة أساسيان لأي قرار عسكري في العصر الرقمي",
                "القانون الدولي الإنساني يوفر إطاراً مهماً لكنه يحتاج لتفسير حكيم",
                "حماية المدنيين تبقى الأولوية القصوى حتى في أوقات الحرب"
            ]
            lesson_index = min(int((100 - overall_score) / 20), 4) if overall_score < 100 else 0
            st.info(f"**{lessons[lesson_index]}**")

# قسم سجل القرارات والمقارنة
st.markdown("---")
st.markdown("## 📋 سجل القرارات والمقارنة")

if st.session_state.decision_history:
    # حساب الإحصائيات
    total_decisions = len(st.session_state.decision_history)
    avg_score_val = sum(d['overall_score'] for d in st.session_state.decision_history) / total_decisions
    best_score_val = max(d['overall_score'] for d in st.session_state.decision_history)
    worst_score_val = min(d['overall_score'] for d in st.session_state.decision_history)
    
    # عرض آخر 5 قرارات
    st.markdown("### آخر القرارات:")
    
    recent_decisions = st.session_state.decision_history[-5:]  # آخر 5 قرارات
    for i, record in enumerate(recent_decisions, 1):
        col_rec1, col_rec2, col_rec3, col_rec4 = st.columns([1, 3, 2, 1])
        
        with col_rec1:
            st.markdown(f"**#{i}**")
        
        with col_rec2:
            scenario_title = record['scenario_title']
            if len(scenario_title) > 30:
                scenario_title = scenario_title[:27] + "..."
            st.markdown(f"**{scenario_title}**")
            st.caption(f"القرار: {record['decision_title']}")
        
        with col_rec3:
            # شريط تقدم صغير
            score = record['overall_score']
            progress_html = f"""
            <div style="width: 100%; background-color: #e9ecef; border-radius: 5px; height: 20px;">
                <div style="width: {score}%; background: linear-gradient(90deg, #28a745, #20c997); 
                         border-radius: 5px; height: 100%;"></div>
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)
        
        with col_rec4:
            color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
            st.markdown(f"<span style='color: {color}; font-weight: bold;'>{score}/100</span>", unsafe_allow_html=True)
    
    # إحصائيات
    st.markdown("### 📊 الإحصائيات:")
    cols_stats = st.columns(4)
    
    with cols_stats[0]:
        st.metric("عدد القرارات", total_decisions)
    with cols_stats[1]:
        st.metric("المتوسط", f"{avg_score_val:.1f}")
    with cols_stats[2]:
        st.metric("أفضل قرار", f"{best_score_val:.1f}")
    with cols_stats[3]:
        st.metric("أسوأ قرار", f"{worst_score_val:.1f}")
    
    # زر مسح السجل
    if st.button("🗑️ مسح سجل القرارات", key="clear_history"):
        st.session_state.decision_history = []
        st.rerun()
else:
    st.info("لم تتخذ أي قرارات بعد. اتخذ قرارك الأول لترى التحليل الكامل!")

# قسم التحدي والإنجازات
st.markdown("---")
st.markdown("## 🏆 التحديات والإنجازات")

# حساب الإحصائيات للتحديات
if st.session_state.decision_history:
    total_decisions = len(st.session_state.decision_history)
    avg_score_val = sum(d['overall_score'] for d in st.session_state.decision_history) / total_decisions
    
    # تحقق من وجود قرارات بدرجة 90+
    has_excellent_decision = any(d['overall_score'] >= 90 for d in st.session_state.decision_history)
    
    # تحقق من تجربة جميع أنواع القرارات
    unique_decisions = len(set(d['decision_id'] for d in st.session_state.decision_history))
    tried_all_decisions = unique_decisions == len(DECISIONS)
else:
    total_decisions = 0
    avg_score_val = 0
    has_excellent_decision = False
    tried_all_decisions = False

# تحديات
challenges = [
    {
        "title": "👑 المبتدئ", 
        "condition": "اتخاذ 3 قرارات", 
        "achieved": total_decisions >= 3,
        "description": "ابدأ رحلتك في اتخاذ القرارات الأخلاقية"
    },
    {
        "title": "🎯 المحلل", 
        "condition": "متوسط نقاط فوق 70", 
        "achieved": avg_score_val >= 70 if total_decisions > 0 else False,
        "description": "اتخاذ قرارات متوسطة إلى جيدة باستمرار"
    },
    {
        "title": "⚖️ القانوني", 
        "condition": "قرار قانوني ممتاز (90+)", 
        "achieved": has_excellent_decision,
        "description": "اتخاذ قرار يلتزم بشكل ممتاز بالقانون الدولي"
    },
    {
        "title": "🤖 الخبير", 
        "condition": f"تجربة {len(DECISIONS)} أنواع قرارات", 
        "achieved": tried_all_decisions,
        "description": "تجربة جميع أنواع القرارات المتاحة"
    },
    {
        "title": "🌟 الأسطوري", 
        "condition": "10 قرارات بمتوسط 80+", 
        "achieved": total_decisions >= 10 and avg_score_val >= 80,
        "description": "اتخاذ قرارات ممتازة باستمرار وبكمية كبيرة"
    }
]

# عرض التحديات
cols_challenges = st.columns(5)
for i, challenge in enumerate(challenges):
    with cols_challenges[i]:
        if challenge["achieved"]:
            st.success(f"✅ {challenge['title']}")
            st.caption(challenge["condition"])
            st.markdown(f'<p style="font-size: 10px; color: #666;">{challenge["description"]}</p>', unsafe_allow_html=True)
        else:
            # حساب التقدم
            progress = 0
            if i == 0:  # المبتدئ
                progress = min(total_decisions / 3 * 100, 100)
            elif i == 1:  # المحلل
                progress = min(avg_score_val, 100) if total_decisions > 0 else 0
            elif i == 2:  # القانوني
                progress = 100 if has_excellent_decision else 0
            elif i == 3:  # الخبير
                progress = (unique_decisions / len(DECISIONS)) * 100 if total_decisions > 0 else 0
            elif i == 4:  # الأسطوري
                decisions_progress = min(total_decisions / 10 * 100, 100)
                score_progress = min(avg_score_val, 100) if total_decisions > 0 else 0
                progress = (decisions_progress * 0.5 + score_progress * 0.5) if total_decisions > 0 else 0
            
            st.info(f"🔒 {challenge['title']}")
            st.caption(challenge["condition"])
            
            # شريط تقدم صغير
            if progress > 0:
                st.progress(progress / 100)
            
            st.markdown(f'<p style="font-size: 10px; color: #666;">{challenge["description"]}</p>', unsafe_allow_html=True)

# عرض تقدم عام
st.markdown("### 📊 تقدمك العام")
if total_decisions > 0:
    col_prog1, col_prog2, col_prog3 = st.columns(3)
    with col_prog1:
        st.metric("القرارات المتخذة", total_decisions)
    with col_prog2:
        st.metric("متوسط النقاط", f"{avg_score_val:.1f}/100")
    with col_prog3:
        completion_rate = sum(1 for c in challenges if c["achieved"]) / len(challenges) * 100
        st.metric("معدل الإنجاز", f"{completion_rate:.1f}%")
else:
    st.info("🚀 اتخذ أول قرار لتبدأ رحلتك!")

# قسم التصدير والتحليل المتقدم
st.markdown("---")
st.markdown("## 📤 التصدير والتحليل المتقدم")

if st.session_state.decision_history:
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        # تحليل الأنماط
        with st.expander("🔍 تحليل أنماط القرارات"):
            # حساب تكرار كل نوع قرار
            decision_counts = {}
            for record in st.session_state.decision_history:
                decision_id = record['decision_id']
                decision_counts[decision_id] = decision_counts.get(decision_id, 0) + 1
            
            st.markdown("**تكرار أنواع القرارات:**")
            for decision_id, count in decision_counts.items():
                decision_name = next((d['title'] for d in DECISIONS if d['id'] == decision_id), "غير معروف")
                st.markdown(f"- {decision_name}: {count} مرات")
            
            # متوسط النقاط لكل سيناريو
            scenario_scores = {}
            for record in st.session_state.decision_history:
                scenario_id = record['scenario_id']
                if scenario_id not in scenario_scores:
                    scenario_scores[scenario_id] = []
                scenario_scores[scenario_id].append(record['overall_score'])
            
            st.markdown("**متوسط النقاط لكل سيناريو:**")
            for scenario_id, scores in scenario_scores.items():
                scenario_name = SCENARIOS[scenario_id]['title'][:20] + "..." if len(SCENARIOS[scenario_id]['title']) > 20 else SCENARIOS[scenario_id]['title']
                avg = sum(scores) / len(scores)
                st.markdown(f"- {scenario_name}: {avg:.1f}/100")
    
    with col_export2:
        # تصدير البيانات
        with st.expander("💾 تصدير البيانات"):
            if st.button("📥 تصدير كملف CSV", key="export_csv"):
                # إنشاء DataFrame
                df_data = []
                for record in st.session_state.decision_history:
                    df_data.append({
                        "السيناريو": record['scenario_title'],
                        "القرار": record['decision_title'],
                        "النتيجة_الإجمالية": record['overall_score'],
                        "النتيجة_القانونية": record.get('legal_score', 'N/A'),
                        "النتيجة_الأخلاقية": record.get('ethical_score', 'N/A'),
                        "النتيجة_العسكرية": record.get('military_score', 'N/A'),
                        "التاريخ": record.get('timestamp', 'N/A')
                    })
                
                df = pd.DataFrame(df_data)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                
                st.download_button(
                    label="⬇️ تحميل ملف CSV",
                    data=csv,
                    file_name="قرارات_الأخلاقيات_العسكرية.csv",
                    mime="text/csv",
                    key="download_csv"
                )
            
            if st.button("📊 إنشاء تقرير ملخص", key="summary_report"):
                st.success("✅ تم إنشاء التقرير بنجاح!")
                
                # ملخص التقرير
                st.markdown("### 📋 تقرير ملخص")
                st.markdown(f"- **عدد القرارات:** {total_decisions}")
                st.markdown(f"- **متوسط النتيجة:** {avg_score_val:.1f}/100")
                st.markdown(f"- **أفضل نتيجة:** {best_score_val:.1f}/100")
                st.markdown(f"- **أسوأ نتيجة:** {worst_score_val:.1f}/100")
                st.markdown(f"- **التحديات المكتملة:** {sum(1 for c in challenges if c['achieved'])}/{len(challenges)}")
                
                # توصيات بناءً على الأداء
                st.markdown("#### 💡 توصيات للتحسين:")
                if avg_score_val < 60:
                    st.markdown("- ركز على فهم القوانين الدولية بشكل أفضل")
                    st.markdown("- فكر في بدائل أكثر أخلاقية للقرارات الصعبة")
                elif avg_score_val < 80:
                    st.markdown("- استمر في تحسين مهارات اتخاذ القرار")
                    st.markdown("- جرب سيناريوهات أكثر تعقيداً")
                else:
                    st.markdown("- أداء ممتاز! يمكنك الآن التركيز على الحالات المعقدة جداً")

# تذييل الصفحة
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <h4>⚖️ نظام محاكاة الأخلاقيات في الحرب الذكية</h4>
    <p><strong>للأغراض البحثية والتعليمية فقط</strong></p>
    <p>💡 الهدف: فهم تعقيدات اتخاذ القرارات الأخلاقية والقانونية والعسكرية في استخدام التقنيات المتقدمة</p>
    <p>📚 المصادر: القانون الدولي الإنساني، أخلاقيات الذكاء الاصطناعي، العلوم العسكرية</p>
    <p>⚠️ تحذير: هذا النظام لا يقدم مشورة قانونية أو عسكرية فعلية</p>
    <p>📅 الإصدار: 1.0.0 | آخر تحديث: يناير 2024</p>
</div>
""", unsafe_allow_html=True)

# تشغيل التطبيق
if __name__ == "__main__":
    # إضافة معرف جلسة
    if 'run_id' not in st.session_state:
        st.session_state.run_id = 0
    st.session_state.run_id += 1