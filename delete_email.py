import imaplib

my_email = "YOUR_EMAIL"
app_generated_password = "YOUR_APP_PASSWORD" #masukin app password (bukan password gmail)



#Inisialisasi Objek Imap menggunakan gmail
imap = imaplib.IMAP4_SSL("imap.gmail.com")

#Login user
imap.login(my_email, app_generated_password)

#menampilkan list
print(imap.list())
"""
('OK', [b'(\\HasNoChildren) "/" "INBOX"', b'(\\HasChildren \\Noselect)
 "/" "[Gmail]"', b'(\\All \\HasNoChildren) "/" "[Gmail]/All Mail"', b'(\\HasNoChildren \\Trash) 
 "/" "[Gmail]/Bin"', b'(\\Drafts \\HasNoChildren) "/" "[Gmail]/Drafts"', b'(\\HasNoChildren \\Important) 
 "/" "[Gmail]/Important"', b'(\\HasNoChildren \\Sent) "/" "[Gmail]/Sent Mail"', b'(\\HasNoChildren \\Junk) 
 "/" "[Gmail]/Spam"', b'(\\Flagged \\HasNoChildren) "/" "[Gmail]/Starred"'])
"""
folderToDeleteEmailsFrom = '"[Gmail]/All Mail"'
trashFolder = '[Gmail]/Bin'

#memilih folder yang mau di delete
imap.select(folderToDeleteEmailsFrom)
gmail_search = '"category:promotions NOT is: important"'

#melakukan pencarian dan mengambil data berdasarkan gmail search yang telah ditentukan
typ, [msg_ids] = imap.search(None, 'X-GM-RAW', gmail_search)

#mengecek apakah terdapat email atau sudah tidak ada
msg_count = len(msg_ids)
print("Found message count: ", msg_count)
if msg_count == 0:
    print("No new messages matching the criteria to be deleted.")
else:
    if isinstance(msg_ids, bytes):
        # if it's a bytes type, decode to str
        msg_ids = msg_ids.decode()

    msg_ids = ','.join(msg_ids.split(' '))
    print("Moving to Trash using X-GM_LABELS.")
    imap.store(msg_ids, '+X-GM-LABELS', '\\Trash')

    # Semua email akan di hapus secara permanen
    print("Emptying Trash and expunge...")
    imap.select(trashFolder)
    imap.store("1:*", '+FLAGS', '\\Deleted')  # menandai semua sampah
    imap.expunge() #menghapus semua email yang terpilih

print("Done")
# tutup mailbox
imap.close()

# logout
imap.logout()