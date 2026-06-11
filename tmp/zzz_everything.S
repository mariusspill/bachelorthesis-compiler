
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
	call	input_int64
	li	t1,2
	mul	a0,a0,t1
	add	s1,zero,a0
	call	input_int64
	li	t1,2
	mul	a0,a0,t1
	j	orelse_1
orelse_1: 
	sub	a1,s1,a0
	sltu	a1,zero,a1
	slli	a1,a1,1
	j	cont_2
cont_2: 
	li	t1,0
	bne	a1,t1,body_3
	j	orelse_4
body_3: 
	beq	s1,a0,body_6
	j	orelse_7
body_6: 
	li	a1,2
	j	cont_8
cont_8: 
	j	cont_5
cont_5: 
	li	t1,0
	bne	a1,t1,body_9
	j	orelse_10
body_9: 
	slt	a3,s1,a0
	slli	a3,a3,1
	slt	a1,a0,s1
	xori	a1,a1,1
	slli	a1,a1,1
	slt	a2,a0,s1
	slli	a2,a2,1
	slt	a4,s1,a0
	xori	a4,a4,1
	slli	a4,a4,1
	j	cont_11
cont_11: 
	li	t1,0
	bne	a3,t1,body_12
	j	orelse_13
body_12: 
	j	cont_14
cont_14: 
	li	t1,0
	bne	a1,t1,body_15
	j	orelse_16
body_15: 
	li	t1,0
	bne	a2,t1,body_18
	j	orelse_19
body_18: 
	add	a1,zero,a4
	j	cont_20
cont_20: 
	j	cont_17
cont_17: 
	li	t1,0
	beq	a1,t1,body_21
	j	orelse_22
body_21: 
	sub	a0,s1,a0
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	j	cont_23
cont_23: 
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
orelse_22: 
	li	a0,0
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	j	cont_23
orelse_19: 
	li	a1,0
	j	cont_20
orelse_16: 
	li	a1,0
	j	cont_17
orelse_13: 
	li	a1,0
	j	cont_14
orelse_10: 
	li	a3,2
	li	a1,2
	li	a2,2
	li	a4,2
	j	cont_11
orelse_7: 
	li	a1,2
	j	cont_8
orelse_4: 
	li	a1,0
	j	cont_5