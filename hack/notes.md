Create EKS Cluster using CDK python and IDF modules

```shell
export PRIMARY_ACCOUNT=123456789
export AWS_REGION=us-east-1
export AWS_USER_OR_ROLE_TO_ASSUME_SEEDFARMER_TOOLCHAIN_ROLE=arn:aws:iam::$PRIMARY_ACCOUNT:user/Administrator
```

```shell
npm install -g aws-cdk
```

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install seed-farmer
cdk bootstrap aws://${PRIMARY_ACCOUNT}/${AWS_REGION}
```

```shell
seedfarmer bootstrap toolchain \
--project exampleproj \
-t ${AWS_USER_OR_ROLE_TO_ASSUME_SEEDFARMER_TOOLCHAIN_ROLE} \
--region us-east-1 \
--as-target
```


```shell
cd examples
echo PRIMARY_ACCOUNT=${PRIMARY_ACCOUNT} >>.env
seedfarmer apply manifests/example/deployment.yaml --env-file .env
```

```shell
seedfarmer list modules -d examples -p exampleproj --region us-east-1
```

```shell
export CLUSTER_NAME=$(aws eks --region ${AWS_REGION} list-clusters --output json | jq -r '.clusters[0]')
```

Use role used to create the cluster
```shell
aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME} \
--role-arn $(seedfarmer list moduledata -d examples -p exampleproj --region us-east-1 -g compute -m eks | jq -r .EksClusterAdminRoleArn)
```


Need to allow to assume roles below

1. Admin role - allows full access to the namespaced and cluster-wide resources of EKS
```shell
export KUBECONFIG=/tmp/${CLUSTER_NAME}
aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME} --role-arn arn:aws:iam::${PRIMARY_ACCOUNT}:role/Admin
```

2. Poweruser role - allows CRUD operations for namespaced resources of the EKS cluster
```shell
export KUBECONFIG=/tmp/${CLUSTER_NAME}
aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME} --role-arn arn:aws:iam::${PRIMARY_ACCOUNT}:role/PowerUser
```

3. Read-only role - allows read operations for namespaced resources of the EKS cluster
```shell
export KUBECONFIG=/tmp/${CLUSTER_NAME}
aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME} --role-arn arn:aws:iam::${PRIMARY_ACCOUNT}:role/ReadOnly
```

Destroy
```shell
seedfarmer destroy examples --region us-east-1 --env-file .env
```

