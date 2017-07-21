import socket
from clockdeco import clock
"""
	Given CoNLL format passed as input, where sentences are split by \n\n, return list of verb:
"""
# user: setup semafor parser to listen at port 8080, import "semafor" from api with reconnect=True

@clock
def semafor(sock, text, reconnect=None):

	if reconnect is not None:
		if sock is not None:
			sock.shutdown(socket.SHUT_WR)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('127.0.0.1', 8080))

	sock.sendall(text.encode('utf8'))
	sock.shutdown(socket.SHUT_WR)

	# retrieve result
	response = []
	while True:
		chunk = sock.recv(8192)
		if not chunk:
			break
		response.append(eval(chunk.decode('utf-8')))
	return response


if __name__ == '__main__':
	from dep_conll_api import setup_parser as corenlp

	# setup parser to listen to 8080
	# base_path = 'D:/Documents/python/NLP/semafor-master/semafor-master/'
	# semafor_jar = base_path + 'target/Semafor-3.0-alpha-04.jar'
	# serverclass = base_path + 'edu.cmu.cs.lti.ark.fn.SemaforSocketServer'
	# model = 'model-dir:' + base_path + 'models/semafor_malt_model_20121129/'
	#
	# # setup parser to listen at port 8000
	# semafor_parser = Popen(
	# 	['java', '-Xms4g', '-Xmx4g', '-cp', semafor_jar, serverclass, model, 'port:8000'])

	CONLL = ['1	My	My	PRP$	PRP$	_	2	NMOD	_	_',
	'2	kitchen	kitchen	NN	NN	_	5	SUB	_	_',
	'3	no	no	RB	RB	_	5	VMOD	_	_',
	'4	longer	longer	RB	RB	_	0	AMOD	_	_',
	'5	smells	smells	VBZ	VBZ	_	0	ROOT	_	_',
	'6	.	.	.	.	_	5	P	_	_']

	CONLL_DATA = """1	We	_	PRP	PRP	_	3	nsubj	_	_
	2	're	_	VB	VBP	_	3	aux	_	_
	3	about	_	IN	IN	_	0	null	_	_
	4	to	_	TO	TO	_	5	aux	_	_
	5	see	_	VB	VB	_	3	xcomp	_	_
	6	if	_	IN	IN	_	8	mark	_	_
	7	advertising	_	NN	NN	_	8	nn	_	_
	8	works	_	NN	NNS	_	5	dobj	_	_
	9	.	_	.	.	_	3	punct	_	_
	"""

	# parse sentences, CONLL_DATA format separated by \n\n
	test2 = "John hits Fred. Then he has a drumstick."
	CONLL_parser = corenlp()
	CONLL_output = CONLL_parser(text=test2, property='conllu')

	# prepare text if format in CONLL
	# split_by_sent = CONLL
	# result = [u'\n'.join(item) for item in split_by_sent]

	# semafor it
	response = semafor(sock=None, text=CONLL_output, reconnect=1)
	print(response)
	# print('ok')