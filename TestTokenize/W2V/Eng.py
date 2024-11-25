from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np

# # Tải stopwords từ NLTK nếu chưa tải
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

# Danh sách stopwords
stopwords_en = set(stopwords.words('english'))
# # Hàm tiền xử lý văn bản: tokenization và loại bỏ stopwords
def preprocess(doc):
    tokens = word_tokenize(doc.lower())  # Tokenize và chuyển thành chữ thường
    return [word for word in tokens if word not in stopwords_en and word.isalnum()]  # Loại bỏ stopwords và ký tự không phải chữ



# Mở và đọc tài liệu
# sample = open("W2V/test.txt", encoding="utf-8")
# s = sample.read()
# # Tiền xử lý tất cả tài liệu
# processed_documents = [preprocess(s)]  # Dữ liệu đầu vào phải là danh sách các câu, mỗi câu là danh sách từ

# # Huấn luyện mô hình Word2Vec
# model = Word2Vec(
#     sentences=processed_documents,  # Cung cấp tài liệu đã được token hóa
#     vector_size=100,                # Kích thước vector
#     window=5,                      # Kích thước cửa sổ ngữ cảnh
#     min_count=1,                   # Bỏ qua từ xuất hiện ít hơn 1 lần
#     workers=4,                     # Số luồng
#     sg=0,                          # Skip-gram (sg=1) hoặc CBOW (sg=0)
#     epochs=10                      # Số lần huấn luyện
# )

# # Kiểm tra độ tương đồng giữa các từ
# def check_similarity(word1, word2, model):
#     if word1 in model.wv and word2 in model.wv:
#         return model.wv.similarity(word1, word2)
#     else:
#         return None

# print("Cosine similarity between 'alice' and 'wonderland': ", check_similarity('alice', 'wonderland', model))
# print("Cosine similarity between 'alice' and 'machines': ", check_similarity('alice', 'machines', model))

# # Biểu diễn câu bằng trung bình vector
# def sentence_vector(sentence, model):
#     tokens = preprocess(sentence)
#     vectors = [model.wv[word] for word in tokens if word in model.wv]
#     if vectors:
#         return np.mean(vectors, axis=0)
#     else:
#         return np.zeros(model.vector_size)

# # Ví dụ: Biểu diễn câu bằng vector
# doc_vector = sentence_vector(s, model)
# print(f"Vector representation for the document:\n{doc_vector}")












documents = [
    "The security team monitors network traffic for suspicious activity.",
    "System administrators patch vulnerabilities in the software regularly.",
    "Firewalls and intrusion detection systems protect the network perimeter.",
    "Encrypting sensitive data is crucial for ensuring privacy.",
    "Regular backups are essential to recover from potential cyberattacks.",
    "Antivirus software helps protect systems from malware and viruses.",
    "Intrusion prevention systems (IPS) monitor network traffic for signs of attacks.",
    "Access control policies restrict unauthorized users from accessing sensitive data.",
    "Encryption algorithms like AES are used to secure data during transmission.",
    "Security patches are applied to software to fix known vulnerabilities.",
    "The firewall blocks incoming traffic from untrusted sources.",
    "Two-factor authentication provides an extra layer of security for users.",
    "Malware analysis helps identify and mitigate harmful software.",
    "Cybersecurity training for employees reduces the risk of human error.",
    "Penetration testing simulates cyberattacks to find security weaknesses.",
    "The secure socket layer (SSL) protocol encrypts communication between websites and users.",
    "Firewalls and antivirus programs work together to protect against online threats.",
    "Data breaches expose sensitive information, leading to privacy concerns.",
    "Network segmentation limits the spread of malicious software across systems.",
    "User access logs help track and monitor user activities on a network.",
    "The principle of least privilege ensures users only have the permissions they need.",
    "Cyber hygiene practices like regular software updates help prevent security incidents.",
    "A distributed denial-of-service (DDoS) attack overwhelms a system with traffic.",
    "The zero-trust security model requires verification of every user and device.",
    "Social engineering attacks manipulate users into revealing confidential information.",
    "Endpoint security protects devices like computers and smartphones from threats.",
    "Security monitoring systems detect and respond to security incidents in real-time.",
    "Threat intelligence feeds provide information about emerging cyber threats.",
    "Secure coding practices help developers write software resistant to attacks.",
    "A VPN (Virtual Private Network) encrypts internet traffic and hides the user's IP address.",
    "Ransomware encrypts a victim’s files and demands payment for decryption.",
    "Phishing attacks attempt to trick users into disclosing personal information.",
    "Data encryption at rest protects stored data from unauthorized access.",
    "Patch management ensures that security vulnerabilities are fixed in a timely manner.",
    "The CIA triad refers to the principles of confidentiality, integrity, and availability.",
    "Botnets are networks of compromised computers used to perform attacks like DDoS.",
    "Security audits assess an organization's security posture and identify risks.",
    "Application security involves securing software from vulnerabilities during development.",
    "Biometric authentication uses physical characteristics like fingerprints or facial recognition.",
    "A honeypot is a decoy system designed to attract and monitor cyberattacks.",
    "The cloud offers scalable solutions for securing data and applications online.",
    "Strong passwords and passphrases are key to protecting user accounts.",
    "Network traffic analysis helps identify suspicious activities and potential threats.",
    "Encryption keys are used to protect sensitive data during encryption and decryption.",
    "Security information and event management (SIEM) systems collect and analyze security data.",
    "Digital forensics involves investigating cybercrimes and retrieving evidence from systems.",
    "Privileged access management controls access to critical systems and data.",
    "Mobile device management (MDM) secures and manages mobile devices within an organization.",
    "Identity and access management (IAM) systems ensure proper user authentication and authorization.",
    "Security breaches can lead to financial loss, reputational damage, and legal consequences.",
    "Data loss prevention (DLP) systems prevent unauthorized access to sensitive data.",
    "A security operations center (SOC) monitors and responds to security incidents 24/7.",
    "A security policy defines the rules and guidelines for maintaining cybersecurity within an organization.",
    "Cyber insurance helps protect organizations financially against the impact of cyberattacks.",
    "Network monitoring tools help detect anomalies and potential security threats.",
    "Cloud security ensures that data stored on cloud platforms is protected from unauthorized access.",
    "Data masking hides sensitive data elements from unauthorized users while retaining usability.",
    "Security patches fix vulnerabilities and reduce the risk of exploitation.",
    "Threat hunting involves actively searching for signs of potential threats within a network.",
    "A cybersecurity framework provides a structured approach to securing information systems.",
    "Incident response plans help organizations quickly recover from security incidents.",
    "A secure coding standard outlines best practices for writing secure software.",
    "Application firewalls protect web applications by filtering and monitoring HTTP traffic.",
    "Data integrity checks ensure that data has not been altered or tampered with.",
    "A vulnerability assessment scans systems for known weaknesses and potential risks.",
    "Distributed ledger technology (DLT) enhances security through decentralized data management.",
    "Blockchain technology provides secure, immutable records of transactions.",
    "Access management controls who can view or modify specific resources on a network.",
    "Deep packet inspection (DPI) analyzes network traffic at a granular level to detect attacks.",
    "Multi-factor authentication requires users to provide multiple forms of identification.",
    "Digital signatures authenticate the origin and integrity of electronic documents.",
    "Password managers securely store and manage user passwords for easier access.",
    "Security tokens are physical devices or software used for authentication.",
    "Endpoint detection and response (EDR) tools monitor and respond to threats on endpoints.",
    "A cyberattack can disrupt business operations and damage an organization’s reputation.",
    "Doxxing involves publicly revealing personal information about an individual without consent.",
    "A web application firewall (WAF) protects applications from malicious traffic and attacks.",
    "Privacy laws like GDPR regulate how personal data is collected, stored, and shared.",
    "A security breach notification system informs users when their data has been compromised.",
    "Cloud access security brokers (CASB) help organizations secure their use of cloud services.",
    "Zero-day vulnerabilities are security flaws that are unknown to the software vendor.",
    "Security encryption methods like RSA and AES ensure safe communication and data storage.",
    "An SSL certificate authenticates the identity of a website and encrypts communication.",
    "Advanced persistent threats (APT) are long-term, targeted cyberattacks aimed at stealing sensitive data.",
    "Cyber threat actors may include hackers, criminal organizations, and nation-state adversaries.",
    "The NIST Cybersecurity Framework provides guidelines for managing cybersecurity risks.",
    "A penetration testing tool automates the process of testing system vulnerabilities.",
    "Malware prevention software can identify, block, and remove malicious software from systems.",
    "A vulnerability management program helps identify, assess, and remediate security risks.",
    "An attack surface represents the total number of points where an attacker can access a system.",
    "Two-factor authentication (2FA) is a security measure requiring two forms of identification.",
    "Adversarial machine learning involves manipulating machine learning models to bypass security measures.",
    "Decryption reverses the process of encryption, restoring data to its original form.",
    "A security incident response plan provides procedures for handling and mitigating cybersecurity events.",
    "Artificial intelligence (AI) is increasingly used to detect and respond to cybersecurity threats.",
    "A security patch is a software update designed to fix known security vulnerabilities.",
    "Cybersecurity frameworks provide best practices for identifying, managing, and mitigating risks.",
    "Risk management identifies potential risks and implements measures to reduce or eliminate them.",
    "Security awareness training educates employees on recognizing and avoiding security threats.",
    "A backup strategy ensures that critical data is regularly copied and can be restored in case of loss.",
    "The dark web is a hidden part of the internet often used for illicit activities.",
    "Ransomware attacks lock users out of their systems or encrypt their data until a ransom is paid.",
    "The principle of defense in depth involves using multiple layers of security to protect systems.",
    "Public key infrastructure (PKI) is used to manage digital keys and certificates for secure communication.",
    "Data classification involves categorizing data based on its sensitivity and importance.",
    "Security governance ensures that cybersecurity strategies align with business objectives.",
    "The principle of separation of duties reduces the risk of fraud and errors by dividing responsibilities.",
    "A security risk assessment identifies vulnerabilities and potential threats to an organization's assets.",
    "Zero trust security means no user or device is trusted by default and must be verified continuously.",
    "Security operations teams analyze logs and alerts to identify suspicious activities or incidents.",
    "Cloud service providers ensure that cloud infrastructure is secure from attacks and breaches.",
    "A data breach is the unauthorized access or disclosure of confidential or protected data.",
    "Security scanning tools automatically scan systems for vulnerabilities and configuration issues.",
    "A botnet is a group of compromised devices used to carry out large-scale cyberattacks.",
    "Advanced firewalls inspect traffic and block malicious content to protect networks.",
    "Secure software development practices reduce the risk of vulnerabilities in applications.",
    "A data breach notification process informs users and regulators when personal data is compromised.",
    "Application security tools identify vulnerabilities in code during development to prevent security issues.",
    "End-to-end encryption ensures that data is encrypted during transmission and storage, preventing unauthorized access."
]

# Hàm tiền xử lý văn bản: tokenization và loại bỏ stopwords
def preprocess(doc):
    tokens = word_tokenize(doc.lower())  # Tokenize và chuyển thành chữ thường
    return [word for word in tokens if word not in stopwords_en and word.isalnum()]  # Loại bỏ stopwords và ký tự không phải chữ

# Tiền xử lý tất cả tài liệu
processed_documents = [preprocess(doc) for doc in documents]

# Huấn luyện mô hình Word2Vec
model = Word2Vec(
    sentences=processed_documents,  # Cung cấp tài liệu đã được token hóa
    vector_size=500,                # Kích thước vector
    window=5,                       # Kích thước cửa sổ ngữ cảnh
    min_count=1,                    # Bỏ qua từ xuất hiện ít hơn 1 lần
    workers=4,                      # Số luồng
    sg=0,                           # Skip-gram (sg=1) hoặc CBOW (sg=0)
    epochs=40                       # Số lần huấn luyện
)

# Tính độ tương đồng giữa các từ
print("Cosine similarity between 'security' and 'activity': ",
      model.wv.similarity('security', 'activity'))

print("Cosine similarity between 'system' and 'software': ",
      model.wv.similarity('system', 'software'))

word_to_check = 'system'

# Kiểm tra nếu từ có trong từ điển
if word_to_check in model.wv:
    # Lấy danh sách tất cả các từ trong mô hình
    all_words = list(model.wv.index_to_key)
    
    # Tính cosine similarity giữa từ 'word_to_check' và tất cả các từ khác trong từ điển
    similarity_scores = []
    for word in all_words:
        similarity = model.wv.similarity(word_to_check, word)
        similarity_scores.append((word, similarity))
    
    # Sắp xếp các từ theo độ tương quan tăng dần và lấy từ có độ tương quan thấp nhất
    least_related_word = min(similarity_scores, key=lambda x: x[1])
    print(f"The word least related to '{word_to_check}' is '{least_related_word[0]}' with a similarity of {least_related_word[1]}")
else:
    print(f"The word '{word_to_check}' is not in the vocabulary.")

# Biểu diễn câu bằng trung bình vector
def sentence_vector(sentence, model):
    tokens = preprocess(sentence)
    vectors = [model.wv[word] for word in tokens if word in model.wv]
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(model.vector_size)

# Biểu diễn tài liệu đầu tiên
doc_vector = sentence_vector(documents[0], model)
# print(f"Vector representation for the first document:\n{doc_vector}")
print(model.wv['security'])

