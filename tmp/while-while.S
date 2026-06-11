
	.globl	main
	.align	8
main: 
	addi	sp,sp,-112
	sd	zero,0(sp)
	sd	ra,104(sp)
	sd	fp,96(sp)
	addi	fp,sp,112
	sd	s3,-24(fp)
	sd	s2,-32(fp)
	sd	s6,-40(fp)
	sd	s11,-48(fp)
	sd	s1,-56(fp)
	sd	s4,-64(fp)
	sd	s9,-72(fp)
	sd	s8,-80(fp)
	sd	s5,-88(fp)
	sd	s10,-96(fp)
	sd	s7,-104(fp)
	add	s3,zero,zero
	add	s2,zero,zero
	add	s6,zero,zero
	add	s11,zero,zero
	add	s1,zero,zero
	add	s4,zero,zero
	add	s9,zero,zero
	add	s8,zero,zero
	add	s5,zero,zero
	add	s10,zero,zero
	add	s7,zero,zero
	addi	a0,fp,-104
	li	a1,8
	call	gc_init
	j	main_start
main_start: 
	li	s2,0
	call	input_int64
	li	t1,2
	mul	a0,a0,t1
	add	s1,zero,a0
	call	input_int64
	li	t1,2
	mul	a0,a0,t1
	add	a1,zero,a0
	li	a2,2
	j	test_0
test_0: 
	bge	s1,a2,body_1
	j	cont_2
body_1: 
	li	a0,2
	j	test_3
test_3: 
	bge	a1,a0,body_4
	j	cont_5
body_4: 
	add	a3,s2,a2
	add	s2,a3,a0
	addi	a0,a0,2
	j	test_3
cont_5: 
	addi	a2,a2,2
	j	test_0
cont_2: 
	add	a0,zero,s2
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	j	main_conclusion
main_conclusion: 
	ld	s3,-24(fp)
	ld	s2,-32(fp)
	ld	s6,-40(fp)
	ld	s11,-48(fp)
	ld	s1,-56(fp)
	ld	s4,-64(fp)
	ld	s9,-72(fp)
	ld	s8,-80(fp)
	ld	s5,-88(fp)
	ld	s10,-96(fp)
	ld	s7,-104(fp)
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,112
	addi	a0,zero,0
	ret