HIGH_BLOOD_PROMPT = """
Q1 [Multiple Choice]: Did you measure your blood pressure today?
Choices:
Yes
No
If the user selects Yes:
Q1.1 [Free Text]: Please tell us the measured blood pressure. 
(e.g., "130/80 mmHg")
Q1.1.1 [Multiple Choice]: Compared to your usual values, was this higher, lower, or similar?  Choices:
Higher
Similar
Lower
If the user selects Higher:  Q1.1.1.1 [Free Text]: What might have caused the high reading? (Example: "I drank a lot at a company dinner last night.")  Proceed to Q1.1.2
If the user selects Similar:  Proceed to Q1.1.2
If the user selects Lower:  Q1.1.1.2 [Multiple Choice]: Did you experience dizziness or discomfort related to the lower reading?  Choices:
Yes
No
If the user selects Yes:  Q1.1.1.2.1 [Free Text]: Please describe any symptoms or discomfort you experienced.  Proceed to Q1.1.2
If the user selects No:  Proceed to Q1.1.2
Q1.1.2 [Free Text]: Were there any special conditions during the measurement? (e.g., posture, resting beforehand)  Proceed to Q1.2
Q1.2 [Multiple Choice]: When did you measure your blood pressure? Choices:
Morning (before medication)
Evening
Other
If the user selects Other:  Q1.2.1 [Free Text]: Please specify when you measured it. (Example: "Right after exercising.")  Proceed to Q2
If the user selects any other option:  Proceed to Q2
If the user selects No:  Q2.1 [Free Text]: Please tell us why you didn’t measure your blood pressure today.  Proceed to Q2.2
Q2.2 [Multiple Choice]: Would you like to record other health information (e.g., medication or lifestyle changes)?  Choices:
Yes
No
If the user selects Yes:
Q3 [Multiple Choice]: Did you take your hypertension medication today?  Choices:
Yes
No
If the user selects Yes:  Q3.1 [Multiple Choice]: Did you experience any side effects?  Choices:
Yes
No
If the user selects Yes:  Q3.1.1 [Free Text]: What symptoms did you experience? (Example: "I felt my ankles swelling slightly.")  Proceed to Q5
If the user selects No:  Proceed to Q5
If the user selects No:  Q4.1 [Free Text]: Please tell us why you did not take your medication. (Example: "I forgot because the morning was hectic.")  Proceed to Q5
If the user selects No to Q2.2:  Proceed to Q5
Q5 [Multiple Choice]: Did you make any lifestyle changes today (e.g., diet, exercise, stress)?  Choices:
Yes
No
If the user selects Yes:  Q5.1 [Multiple Choice]: What changes occurred?  Choices:
Diet
Exercise
Alcohol/Smoking
Stress/Sleep
If Diet:  Q5.1.1 [Free Text]: Describe the dietary change. (Example: "I ate out and had salty food.")
If Exercise:  Q5.1.2 [Free Text]: What kind of exercise did you do and for how long? (Example: "I skipped exercise because I was tired.")
If Alcohol/Smoking:  Q5.1.3 [Multiple Choice]: What kind of change occurred?  Choices:
Reduced or quit drinking
Drank more than usual
Quit smoking
Smoked more or less
If Smoked more or less:  Q5.1.3.1 [Free Text]: Please describe the change. (Example: "I smoked more than usual because I was stressed.")
If Stress/Sleep: Q5.1.4 [Free Text]: Describe any changes in stress or sleep. (Example: "I was stressed due to a project deadline.") Proceed to Q6
If the user selects No to Q5: Proceed to Q6
Q6 [Multiple Choice]: Did you experience any unusual symptoms today (e.g., dizziness, headache, chest tightness, blurred vision)? Choices:
Yes
No
If the user selects Yes: Q6.1 [Free Text]: Please describe the symptoms, when they started, and how long they lasted. (Example: "Since the afternoon, I’ve had a dull headache and dizziness.")
Q6.1.1 [Multiple Choice]: How severe were the symptoms? Choices:
Mild
Moderate
Severe
If the user selects Severe: Q6.1.1.1 [Multiple Choice]: Your symptoms sound intense. It's a good idea to consider visiting a medical professional. Would you like to add anything else? Choices:
Yes → Proceed to free-text input or new flow
No → Stop
If the user selects Mild or Moderate:  Stop
If the user selects No to Q6: Stop
"""

# Placeholder flows for other diseases
DEPRESSION_PROMPT = """
Q1 [Multiple Choice]: How was your mood today?
Choices:
Very depressed
Somewhat low
Neutral
Good
Very good
If the user selects any option:  Q1.1 [Free Text]: Could you tell me why you felt that way?  (Example: "I felt lonely all day.", "I was happy because I got good news.")
Q2 [Multiple Choice]: Did you feel enjoyment or interest in things you usually like?
Choices:
Not at all
Slightly
Moderately
Fully enjoyed
If the user selects any option:  Q2.1 [Free Text]: If something felt less enjoyable, please describe.  (Example: "Even my favorite show felt boring.")
Q3 [Multiple Choice]: How was your sleep today?
Choices:
Slept well
Hard to fall asleep
Woke up often
Slept too much
If the user selects any option:  Q3.1 [Free Text]: How many hours did you sleep?  (Example: "6 hours but woke up three times.")
Q4 [Multiple Choice]: How was your energy level today?
Choices:
Very low
Somewhat tired
Normal
Energized
If the user selects any option:  Q4.1 [Free Text]: Any notable activity today?  (Example: "Just lay in bed all day.", "Went grocery shopping.")
Q5 [Multiple Choice]: Did you have thoughts of self-harm or suicide today?
Choices:
Frequently
Occasionally
Not at all
If the user selects "Frequently":  → Respond: "This is an emergency. Please contact a professional immediately." → Stop
If the user selects "Occasionally":  Q5.1 [Free Text]: When and why did those thoughts arise?  (Example: "I felt overwhelmed by small things.")
If the user selects "Not at all":  → Stop
Q6 [Multiple Choice]: Did you take your prescribed medication today?
Choices:
All taken
Partially taken
Not taken
If the user selects "Partially taken" or "Not taken":  Q6.1 [Free Text]: If not taken, please explain why.  (Example: "I forgot.", "I felt nauseous.")
Q7 [Multiple Choice]: Did you experience any physical discomfort (e.g., headache, stomach issues)?
Choices:
Yes
No
If the user selects "Yes":  Q7.1 [Free Text]: Please describe the symptom and when it started.  (Example: "Had a headache since morning.")
If the user selects "No":  → Stop
Q8 [Multiple Choice]: How was your appetite and meals today?
Choices:
Loss of appetite
Increased appetite
Skipped meals
Normal
If the user selects any option:  Q8.1 [Free Text]: Any additional note about meals?  (Example: "Only had ramen today.")
Q8.2 [Multiple Choice]: Would you like to record your weight?
Choices:
Yes
No
If the user selects "Yes":  Q8.2.1 [Free Text]: Enter your weight today (e.g., "53.2kg")
If the user selects "No":  → Stop
Q9 [Multiple Choice]: Did you feel your concentration or memory declined today?
Choices:
Often
Slightly
Not at all
→ Stop
Q10 [Multiple Choice]: Did you interact with others today?
Choices:
Was alone
Only exchanged messages
Met someone
Met several people
If the user selects any option:  Q10.1 [Free Text]: How did you feel after the interaction?  (Example: "It was refreshing.", "It drained my energy.")
"""

ASTHMA_PROMPT = """
Q1 [Multiple Choice]: Have you felt shortness of breath today or in the past few days?
Choices:
Yes
No
If the user selects Yes:
Q1.1 [Multiple Choice]: When do the symptoms usually occur?  Choices:
During exercise
At night while sleeping
Other
Q1.2 [Free Text]: Please describe the symptoms you experienced. (Example: “I felt very breathless after exercising.”)
Q1.3 [Multiple Choice]: Did you use any emergency medication (e.g., Salbutamol, Fenoterol) or visit a hospital or emergency room?  Choices:
Yes
No
Proceed to Q2
If the user selects No:  Proceed to Q2

Q2 [Multiple Choice]: Did you take your prescribed medication today?  Choices:
Took all
Took partially
Did not take
If the user selects Took all:  Q2.1 [Multiple Choice]: Did you take any emergency medication today?  Choices:
Yes → Stop
No → Stop
If the user selects Took partially or Did not take:  Q2.1 [Free Text]: Please explain why you didn’t take the medication.  (Example: “I had stomach discomfort, so I skipped it.”)  → Stop

Q3 [Multiple Choice]: Have you experienced any uncomfortable symptoms after taking your medication recently?  Choices:
Yes
No → Stop
If the user selects Yes:  Q3.1 [Free Text]: What symptoms did you experience?  (Example: “My throat felt irritated.”)  → Stop

Q4 [Multiple Choice]: Did you measure your oxygen saturation today?  Choices:
Yes
No → Stop
If the user selects Yes:  Q4.1 [Free Text]: What was your oxygen saturation level?  (Example: “96%.”)  → Stop

Q5 [Multiple Choice]: Did you measure your Peak Expiratory Flow (PEF) today?  Choices:
Yes
No → Stop
If the user selects Yes:  Q5.1 [Free Text]: What was your peak flow rate in liters per minute?  (Example: “420 L/min.”)  → Stop
"""
