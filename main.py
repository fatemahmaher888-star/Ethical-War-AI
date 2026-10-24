"""
نظام محاكاة الأخلاقيات في الذكاء الاصطناعي العسكري
إصدار مبسط وسهل التعديل
"""

def main():
    print("=" * 50)
    print("نظام محاكاة الأخلاقيات في الحرب الذكية")
    print("=" * 50)
    
    # عرض قائمة السيناريوهات
    scenarios = [
        {"id": 1, "name": "مستودع أسلحة في صحراء", "difficulty": "سهل"},
        {"id": 2, "name": "مقر عسكري في مدينة", "difficulty": "متوسط"},
        {"id": 3, "name": "مدرسة مشتبه بها", "difficulty": "صعب"}
    ]
    
    print("\nاختر سيناريو:")
    for sc in scenarios:
        print(f"{sc['id']}. {sc['name']} ({sc['difficulty']})")
    
    choice = input("\nادخل رقم السيناريو (1-3): ")
    
    # تشغيل السيناريو المختار
    run_scenario(int(choice))

def run_scenario(scenario_id):
    """تشغيل سيناريو معين"""
    
    # بيانات السيناريوهات (مبسطة)
    scenarios_data = {
        1: {
            "title": "مستودع أسلحة في صحراء",
            "description": "مستودع أسلحة مؤكد في منطقة صحراوية غير مأهولة",
            "military_value": 90,  # قيمة عسكرية (0-100)
            "civilian_risk": 5,    # خطر مدني (0-100)
            "certainty": 95,       # درجة التأكد (0-100)
            "time_pressure": 20    # ضغط الوقت (0-100)
        },
        2: {
            "title": "مقر عسكري في مدينة",
            "description": "مقر قيادة في منطقة سكنية",
            "military_value": 80,
            "civilian_risk": 60,
            "certainty": 70,
            "time_pressure": 50
        },
        3: {
            "title": "مدرسة مشتبه بها",
            "description": "مدرسة يُشتبه في استخدامها كمقر عسكري",
            "military_value": 70,
            "civilian_risk": 85,
            "certainty": 40,
            "time_pressure": 30
        }
    }
    
    if scenario_id not in scenarios_data:
        print("سيناريو غير موجود!")
        return
    
    data = scenarios_data[scenario_id]
    
    print("\n" + "=" * 50)
    print(f"السيناريو: {data['title']}")
    print("=" * 50)
    print(f"الوصف: {data['description']}")
    print(f"\nالمعلومات المتاحة:")
    print(f"- القيمة العسكرية: {data['military_value']}/100")
    print(f"- الخطر المدني: {data['civilian_risk']}/100")
    print(f"- درجة التأكد: {data['certainty']}/100")
    print(f"- ضغط الوقت: {data['time_pressure']}/100")
    
    # طرح الخيارات
    print("\n" + "-" * 50)
    print("خياراتك:")
    print("1. ✅ تنفيذ الضربة فوراً")
    print("2. 🔍 طلب معلومات إضافية")
    print("3. 🤖 ترك القرار للذكاء الاصطناعي")
    print("4. ❌ رفض الضربة")
    
    decision = input("\nاختر قرارك (1-4): ")
    
    # تحليل القرار
    analyze_decision(decision, data)

def analyze_decision(decision, scenario_data):
    """تحليل القرار وإعطاء تقييم أخلاقي"""
    
    ethical_score = 100  # درجة أخلاقية ابتدائية
    
    print("\n" + "=" * 50)
    print("تحليل القرار الأخلاقي")
    print("=" * 50)
    
    if decision == "1":  # تنفيذ فوري
        print("القرار: تنفيذ الضربة فوراً")
        
        # حسابات أخلاقية مبسطة
        if scenario_data['civilian_risk'] > 50:
            ethical_score -= 40
            print("⚠️  خصم 40 نقطة: خطر مدني مرتفع")
        
        if scenario_data['certainty'] < 80:
            ethical_score -= 30
            print("⚠️  خصم 30 نقطة: درجة تأكد منخفضة")
            
        ethical_score -= scenario_data['time_pressure'] / 10
        print(f"⚠️  خصم {scenario_data['time_pressure']/10:.1f} نقطة: ضغط الوقت")
        
    elif decision == "2":  # طلب معلومات
        print("القرار: طلب معلومات إضافية")
        ethical_score -= 10  # خصم بسيط للتأخير
        ethical_score += 20  # مكافأة للحذر
        print("✓ إضافة 20 نقطة: الحذر والتحقق")
        
    elif decision == "3":  # ترك القرار للذكاء الاصطناعي
        print("القرار: تفويض القرار للذكاء الاصطناعي")
        
        # قواعد تفويض مبسطة
        if scenario_data['civilian_risk'] > 30:
            ethical_score -= 50
            print("⚠️  خصم 50 نقطة: لا تفويض قرارات ذات خطر مدني")
        else:
            ethical_score += 10
            print("✓ إضافة 10 نقاط: تفويض مناسب")
            
    elif decision == "4":  # رفض الضربة
        print("القرار: رفض الضربة")
        if scenario_data['military_value'] > 70:
            ethical_score -= 20
            print("⚠️  خصم 20 نقطة: فقدان فرصة عسكرية مهمة")
        else:
            ethical_score += 30
            print("✓ إضافة 30 نقطة: حماية المدنيين أولوية")
    
    # التأكد من أن النتيجة بين 0 و100
    ethical_score = max(0, min(100, ethical_score))
    
    # عرض النتيجة النهائية
    print("\n" + "-" * 50)
    print(f"النتيجة الأخلاقية: {ethical_score:.1f}/100")
    
    # شريط التقدم البصري
    bars = int(ethical_score / 5)
    print(f"[{'█' * bars}{'░' * (20 - bars)}]")
    
    # التوصية
    if ethical_score >= 80:
        print("✅ قرار أخلاقي ممتاز")
    elif ethical_score >= 60:
        print("☑️ قرار أخلاقي مقبول")
    elif ethical_score >= 40:
        print("⚠️ قرار يحتاج مراجعة")
    else:
        print("❌ قرار غير أخلاقي")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()