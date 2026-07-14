
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
	li	a1,4
	call	gc_init
	j	main_start
main_start: 
	la	a1,gc_free_ptr
	ld	a1,0(a1)
	addi	a2,a1,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a2,a1,body_0
	j	orelse_1
body_0: 
	j	cont_2
cont_2: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a1,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,16
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,6
	sd	t0,-1(a1)
	li	a2,4614253070214989087
	add	t0,zero,a2
	sd	t0,7(a1)
	add	t0,zero,a1
	sd	t0,-112(fp)
	la	a1,gc_free_ptr
	ld	a1,0(a1)
	addi	a2,a1,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a2,a1,body_3
	j	orelse_4
body_3: 
	j	cont_5
cont_5: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a1,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,16
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,6
	sd	t0,-1(a1)
	li	a2,4607182418800017408
	add	t0,zero,a2
	sd	t0,7(a1)
	ld	a2,-112(fp)
	ld	a2,7(a2)
	ld	a1,7(a1)
	fmv.d.x	fa0,a2
	fmv.d.x	fa1,a1
	flt.d	a1,fa1,fa0
	slli	a1,a1,1
	li	t1,0
	bne	a1,t1,body_6
	j	orelse_7
body_6: 
	la	a1,gc_free_ptr
	ld	a1,0(a1)
	addi	a2,a1,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a2,a1,body_9
	j	orelse_10
body_9: 
	j	cont_11
cont_11: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a1,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,16
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,6
	sd	t0,-1(a1)
	li	a2,4617315517961601024
	add	t0,zero,a2
	sd	t0,7(a1)
	ld	a2,-112(fp)
	ld	a2,7(a2)
	ld	a1,7(a1)
	fmv.d.x	fa0,a2
	fmv.d.x	fa1,a1
	flt.d	a1,fa0,fa1
	slli	a1,a1,1
	j	cont_8
cont_8: 
	li	t1,0
	bne	a1,t1,body_12
	j	orelse_13
body_12: 
	ld	a1,-112(fp)
	ld	a1,7(a1)
	fmv.d.x	fa0,a1
	call	print_float
	j	cont_14
cont_14: 
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
orelse_13: 
	j	cont_14
orelse_10: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_11
orelse_7: 
	li	a1,0
	j	cont_8
orelse_4: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_5
orelse_1: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_2