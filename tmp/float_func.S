
	.globl	float_add
	.align	8
float_add: 
	addi	sp,sp,-32
	sd	zero,8(sp)
	sd	ra,24(sp)
	sd	fp,16(sp)
	addi	fp,sp,32
	j	float_add_start
float_add_start: 
	add	a0,zero,a1
	add	a1,zero,a2
	add	t0,zero,a0
	sd	t0,-32(fp)
	add	t0,zero,a1
	sd	t0,-24(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_0
	j	orelse_1
body_0: 
	j	cont_2
cont_2: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a0,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,16
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,6
	sd	t0,-1(a0)
	ld	a1,-32(fp)
	ld	a1,7(a1)
	ld	a2,-24(fp)
	ld	a2,7(a2)
	fmv.d.x	fa0,a1
	add	a1,zero,a2
	fmv.d.x	fa1,a1
	fadd.d	fa0,fa0,fa1
	fmv.x.d	a1,fa0
	add	t0,zero,a1
	sd	t0,7(a0)
	j	float_add_conclusion
	j	float_add_conclusion
float_add_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	ret
orelse_1: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_2

	.globl	main
	.align	8
main: 
	addi	sp,sp,-128
	sd	zero,16(sp)
	sd	ra,120(sp)
	sd	fp,112(sp)
	addi	fp,sp,128
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
	la	t0,float_add
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_3
	j	orelse_4
body_3: 
	j	cont_5
cont_5: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a0,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,16
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,4
	sd	t0,-1(a0)
	ld	t0,-112(fp)
	sd	t0,7(a0)
	add	t0,zero,a0
	sd	t0,-112(fp)
	ld	t0,-112(fp)
	ld	t0,7(t0)
	sd	t0,-120(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_6
	j	orelse_7
body_6: 
	j	cont_8
cont_8: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a0,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,16
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,6
	sd	t0,-1(a0)
	add	t0,zero,a0
	sd	t0,-128(fp)
	li	a0,4614253070214989087
	add	t0,zero,a0
	ld	t1,-128(fp)
	sd	t0,7(t1)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_9
	j	orelse_10
body_9: 
	j	cont_11
cont_11: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a0,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,16
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,6
	sd	t0,-1(a0)
	add	a2,zero,a0
	li	a0,4614253070214989087
	add	t0,zero,a0
	sd	t0,7(a2)
	ld	a0,-112(fp)
	ld	a1,-128(fp)
	ld	t0,-120(fp)
	jalr	t0
	ld	a1,7(a0)
	fmv.d.x	fa0,a1
	call	print_float
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
	addi	sp,sp,128
	addi	a0,zero,0
	ret
orelse_10: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_11
orelse_7: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_8
orelse_4: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_5