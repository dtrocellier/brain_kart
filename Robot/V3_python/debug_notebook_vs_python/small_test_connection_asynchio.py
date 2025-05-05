from tdmclient import ClientAsync, aw

client = ClientAsync()

print(client.tdm_addr)
print(client.tdm_port)

client.process_waiting_messages()

node = client.nodes[0]

node = aw(client.wait_for_node())

print(node)