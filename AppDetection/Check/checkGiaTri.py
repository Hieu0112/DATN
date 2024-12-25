tn = int(input("Nhập giá trị True Negative (TN): "))
fp = int(input("Nhập giá trị False Positive (FP): "))
fn = int(input("Nhập giá trị False Negative (FN): "))
tp = int(input("Nhập giá trị True Positive (TP): "))

ACC=(tp+tn)/(tp+fp+tn+fn)*100
PPV=tp/(tp+fp)*100
TPR=tp/(tp+fn)*100
FPR=fp/(fp+tn)*100
FNR=fn/(tp+fn)*100
f1=(2*tp)/(2*tp+fp+fn)*100
print(f"{ACC:.2f}")  # In ACC
print(f"{PPV:.2f}")  # In PPV
print(f"{TPR:.2f}")  # In TPR
print(f"{f1:.2f}")   # In F1
print(f"{FPR:.2f}")  # In FPR
print(f"{FNR:.2f}")  # In FNR