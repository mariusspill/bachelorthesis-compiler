
	.globl	RGB
	.align	8
RGB: 
	addi	sp,sp,-48
	sd	zero,24(sp)
	sd	zero,16(sp)
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,40(sp)
	sd	fp,32(sp)
	addi	fp,sp,48
	j	RGB_start
RGB_start: 
	add	a0,zero,a1
	add	a1,zero,a3
	add	t0,zero,a0
	sd	t0,-32(fp)
	add	t0,zero,a2
	sd	t0,-40(fp)
	add	t0,zero,a1
	sd	t0,-24(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,32
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_0
	j	orelse_1
body_0: 
	j	cont_2
cont_2: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a0,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,32
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,6
	sd	t0,-1(a0)
	ld	t0,-32(fp)
	sd	t0,7(a0)
	ld	t0,-40(fp)
	sd	t0,15(a0)
	ld	t0,-24(fp)
	sd	t0,23(a0)
	j	RGB_conclusion
	j	RGB_conclusion
RGB_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,48
	ret
orelse_1: 
	add	a0,zero,sp
	li	a1,4
	call	gc_collect
	j	cont_2

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
	la	t0,RGB
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
	li	t0,2
	sd	t0,-1(a0)
	ld	t0,-112(fp)
	sd	t0,7(a0)
	ld	a4,7(a0)
	li	a1,200
	li	a2,48
	li	a3,0
	jalr	a4
	add	s1,zero,a0
	ld	a0,7(s1)
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	ld	a0,15(s1)
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	ld	a0,23(s1)
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
orelse_4: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_5