from models.cert import CertificateRepository
repo = CertificateRepository()

print(repo.get_all_certificates())