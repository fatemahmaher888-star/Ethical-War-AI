# restrictive_algorithm.py
# الخوارزمية التقييدية لضبط صلاحيات الذكاء الاصطناعي في تحديد الأهداف
# Restrictive Targeting Algorithm (RTA)

def apply_restrictive_constraints(scenario_metrics, proposed_decision):
    """
    هذه الخوارزمية تفرض قيوداً قانونية وأخلاقية على القرار المقترح.
    المدخلات:
        scenario_metrics: قاموس يحتوي على (التأكد، الخطر_المدني، القيمة_العسكرية، ضغط_الوقت، الضرورة، التناسب)
        proposed_decision: القرار الذي يريد الذكاء الاصطناعي اتخاذه (1=ضربة فورية، 2=استطلاع، 3=تفويض، 4=رفض)
    المخرجات:
        قرار نهائي (بعد فرض القيود) + سبب التقييد (إن وجد)
    """
    
    # استخراج القيم
    certainty = scenario_metrics.get("التأكد", 0)
    civilian_risk = scenario_metrics.get("الخطر_المدني", 0)
    military_value = scenario_metrics.get("القيمة_العسكرية", 0)
    time_pressure = scenario_metrics.get("ضغط_الوقت", 0)
    necessity = scenario_metrics.get("الضرورة", 0)
    proportionality = scenario_metrics.get("التناسب", 0)
    
    # 1. القيد الأول: مبدأ التمييز (إذا كان التأكد منخفضاً، لا يسمح بالضربة الفورية أو التفويض)
    if certainty < 60:
        if proposed_decision in [1, 3]:  # ضربة فورية أو تفويض
            return {
                "final_decision": 2,  # تحويل القرار إلى استطلاع إضافي
                "restriction_applied": True,
                "reason": f"مبدأ التمييز: درجة التأكد ({certainty}%) أقل من الحد الأدنى (60%). تم تحويل القرار إلى استطلاع إضافي."
            }
    
    # 2. القيد الثاني: مبدأ التناسب (إذا كان الخطر المدني مرتفعاً والتناسب منخفضاً، يمنع الضربة)
    if civilian_risk > 70 and proportionality < 40:
        if proposed_decision == 1:  # ضربة فورية
            return {
                "final_decision": 4,  # رفض الضربة
                "restriction_applied": True,
                "reason": f"مبدأ التناسب: الخطر المدني ({civilian_risk}%) مرتفع جداً والتناسب ({proportionality}%) منخفض. تم رفض الضربة."
            }
    
    # 3. القيد الثالث: منع تفويض الذكاء الاصطناعي في القرارات الحرجة
    if military_value > 80 and civilian_risk > 50:
        if proposed_decision == 3:  # تفويض
            return {
                "final_decision": 2,  # تحويل إلى استطلاع
                "restriction_applied": True,
                "reason": f"قيد المسؤولية البشرية: لا يمكن تفويض قرار عسكري عالي القيمة ({military_value}%) مع خطر مدني مرتفع ({civilian_risk}%). تم تحويل القرار إلى استطلاع."
            }
    
    # 4. القيد الرابع: منع الضربة الفورية في حالات الضغط الزمني المنخفض (يجب استغلال الوقت للتحقق)
    if time_pressure < 30 and proposed_decision == 1:
        return {
            "final_decision": 2,  # استطلاع إضافي
            "restriction_applied": True,
            "reason": f"قيد الاحتياط: ضغط الوقت منخفض ({time_pressure}%)، يجب استغلال الوقت للتحقق الإضافي. تم تحويل القرار إلى استطلاع."
        }
    
    # 5. القيد الخامس: الضرورة العسكرية (إذا كانت الضرورة منخفضة، يمنع أي ضربة)
    if necessity < 50 and proposed_decision in [1, 5]:
        return {
            "final_decision": 4,  # رفض
            "restriction_applied": True,
            "reason": f"قيد الضرورة العسكرية: الضرورة ({necessity}%) غير كافية لتبرير الضربة. تم رفض القرار."
        }
    
    # إذا لم يتم تطبيق أي قيد، يمرر القرار كما هو
    return {
        "final_decision": proposed_decision,
        "restriction_applied": False,
        "reason": "لا توجد قيود مطبقة. القرار مطابق للشروط."
    }
