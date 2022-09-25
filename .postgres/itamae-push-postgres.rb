# coding: utf-8

### postgres用
remote_file "/home/yanagi/postgres/docker-compose.yml" do
    owner "yanagi"
    group "yanagi"
    source "./docker-compose.yml"
end