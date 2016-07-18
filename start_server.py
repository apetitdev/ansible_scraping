# THIS SCRIPT HAS BEEN BUILT IN ORDER TO CREATE A NEW USER TO DEPLOY YOUR APPLICATION ON A UBUNTU SERVER
# THERE ARE A COUPLE OF THINGS THAT NEED TO BE NOTIFIED:
# 1. 	FIRST OF ALL, THIS SCRIPT HAS BEEN CREATED FOR UBUNTU OS, THIS CAN PROBABLY WORKS FOR OTHER LINUX 
#		DISTRIBUTIONS BUT WILL NEED A SMALL UPDATE ON THE FILES PATH
# 2. 	BY DEFAULT, IF YOU DON'T SETTLE IT, THE NEW USER WILL BE NAMED DEPLOYER
# 3. 	BY DEFAULT, IF YOU DON'T SETTLE IT, THE PASWORD FOR THIS NEW USER THE SYSTEM WILL GENERATE ONE
#		AND THIS PASSWORD WILL BE STORED IN A FILE PASSWORD USER ROOT FOLDER

import os
import crypt
import string
import random
import pwd
import grp
import shutil

global password

global deploy_user

global publique_ssh_key

password = ''

deploy_user = ''

publique_ssh_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvZ8qDkE02pbLBt4ljr2r2EF6NghCl6xPUfSXScCjxF/5+1PAJqQ6/7zCQ3tzTVJKuKutU+1870pOCOqKrGfiwtnSZLZXvmEKHxp+042sjVjdf7KDKngd47uOv/zwqKJnd18BNvZ0PY/Y8TRfKXHtwIfHlife2FvzXr3DqpdC+rQKcqXjRFGIxJATDUMaDO190oXgVhFP1DcOfwK7+6SKCMmo0zG1MIj1JZ6+ZhBlJCILE8kzzcdDEYwbU8lwjzztGHSBVxr6aKtj1sieMhDfAQPdCCOVMJ9NRWefXsWZB8SqE11tbi5DlZcf519Bz1epfMSkKQXg0PDskyWl+P7zSWcC+3M3QaKum+V3ykfbqLQZ5v4W431pbNZ4ytdiU/pCNxbHDpk0kAUygY5wG5Hh60jxOTfqsY64dIVtdlObqWfKp6rj/DV9IywY8NSPl2V+xljirFN8QZ+w8IJkOXqKzOp++538W+OdPmtQWCnPi3yqYV7HYFNL0auwJG4/sqcMhpgeuCYh9NTVvh0gUf14zKCtdOzSxW6/SMS18AVG3nL9YsWii0CYk4lnU8gcy5wr1arcDKY1LA8Oj5jS3Ut63Gur0v/QpltwosbqT/z/HnB/sgAmQMn5sk5Rt2sVr2MWt+kmuitwvwmlQwqqz6RgKJTbsT5vDxXActeGonP53OQ== aurelienpetit@eiceducation.com.cn'


class basic_server_settings():

	# Private methods

	def __id_generator(self, size=6, chars=string.ascii_uppercase + string.digits + '!@#$%^&*()_+}{|":?><'):

		return ''.join(random.choice(chars) for _ in range(size))

	def __set_password(self, password):

		if password is None or password == '':

			password = self.__id_generator(36)

		return password

	def __set_deploy_user(self, deploy_user):

		if deploy_user is None or password == '':

			deploy_user = "deployer"

		return deploy_user


	# Public methods

	def create_users(self, deploy_user, password):

		deploy_user = self.__set_deploy_user(deploy_user)

		password = self.__set_password(password)

		encPass = crypt.crypt(password,"22")

		os.system("useradd -p " + encPass + " -s "+ "/bin/bash "+ "-d "+ "/home/" + deploy_user+ " -m "+ " -c \""+ deploy_user+"\" " + deploy_user)

		mode = 'a' if os.path.exists('password.text') else 'w'

		with open("/home/" + str(deploy_user) + "/password.text", mode) as f:

			f.write(password + '\n')

		print 'The user: ', deploy_user, ' has been created with the password: ', password


	def create_ssh_folder_for_deploy_user(self, deploy_user):

		deploy_user = self.__set_deploy_user(deploy_user)

		directory = "/home/" + str(deploy_user) + '/.ssh'

		if not os.path.exists(directory):

			os.makedirs(directory)

			print 'You successfully created you folder: ', directory

		else:

			print 'The folder: ', directory, ' already exists'


	def change_file_owner(self, deploy_user):

		deploy_user = self.__set_deploy_user(deploy_user)

		paths = ["/home/" + str(deploy_user) + "/.ssh","/home/" + str(deploy_user) + '/.ssh/authorized_keys', "/home/" + str(deploy_user) + "/password.text"]

		for path in paths:

			uid = pwd.getpwnam(deploy_user).pw_uid

			gid = grp.getgrnam(deploy_user).gr_gid

			os.chown(path, uid, gid)

			print "you successfully changed the owner to: ", deploy_user, " for the folder: ", path


	def set_up_authorized_key(self, deploy_user, publique_ssh_key):

		deploy_user = self.__set_deploy_user(deploy_user)

		authorized_keys = "/home/" + str(deploy_user) + '/.ssh/authorized_keys'

		if publique_ssh_key is None or publique_ssh_key == '':

			shutil.copy2('/root/.ssh/authorized_keys', '/home/' + deploy_user + '/.ssh/')

			print 'The authorized ssh keys from root have been transfered to: ', deploy_user

		else:

			mode = 'a' if os.path.exists(authorized_keys) else 'w'

			with open(authorized_keys, mode) as f:

				f.write(publique_ssh_key + '\n')

				print 'You successfully added your publique key to the user: ', deploy_user


	def add_deploy_user_to_sudoers(self, deploy_user):

		sudoer_file = '/etc/sudoers'

		deploy_user = self.__set_deploy_user(deploy_user)

		with open(sudoer_file, 'a') as f:

			f.write(deploy_user + '    ALL=(ALL:ALL) NOPASSWD:ALL \n')



Basic_server_settings = basic_server_settings()

Basic_server_settings.create_users(deploy_user, password)

Basic_server_settings.create_ssh_folder_for_deploy_user(deploy_user)

Basic_server_settings.set_up_authorized_key(deploy_user, publique_ssh_key)

Basic_server_settings.change_file_owner(deploy_user)

Basic_server_settings.add_deploy_user_to_sudoers(deploy_user)