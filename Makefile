.PHONY: deploy destroy tf-apply ansible-deploy

deploy: tf-apply ansible-deploy

tf-apply:
	cd terraform && terraform init && terraform apply -auto-approve
	python3 scripts/tf_to_inventory.py

ansible-deploy:
	ansible-playbook -i ansible/inventory/dynamic_inventory.py ansible/playbooks/01_prereqs.yml
	ansible-playbook -i ansible/inventory/dynamic_inventory.py ansible/playbooks/02_deploy_openstack.yml
	ansible-playbook -i ansible/inventory/dynamic_inventory.py ansible/playbooks/03_validate.yml

destroy:
	cd terraform && terraform destroy -auto-approve
