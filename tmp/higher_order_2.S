
	.globl	map
	.align	8
map: 
	addi	sp,sp,-48
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,40(sp)
	sd	fp,32(sp)
	addi	fp,sp,48
	sd	s2,-24(fp)
	sd	s1,-32(fp)
	j	map_start
map_start: 
	add	s2,zero,a1
	add	s1,zero,a2
	add	a0,zero,s2
	ld	a2,7(a0)
	ld	a1,7(s1)
	jalr	a2
	add	t0,zero,a0
	sd	t0,-48(fp)
	add	a0,zero,s2
	ld	a2,7(a0)
	ld	a1,15(s1)
	jalr	a2
	add	t0,zero,a0
	sd	t0,-40(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,24
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_1
	j	orelse_2
body_1: 
	j	cont_3
cont_3: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a0,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,24
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,4
	sd	t0,-1(a0)
	ld	t0,-48(fp)
	sd	t0,7(a0)
	ld	t0,-40(fp)
	sd	t0,15(a0)
	j	map_conclusion
	j	map_conclusion
map_conclusion: 
	ld	s2,-24(fp)
	ld	s1,-32(fp)
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,48
	ret
orelse_2: 
	add	a0,zero,sp
	li	a1,3
	call	gc_collect
	j	cont_3

	.globl	lambda_0
	.align	8
lambda_0: 
	addi	sp,sp,-16
	sd	ra,8(sp)
	sd	fp,0(sp)
	addi	fp,sp,16
	j	lambda_0_start
lambda_0_start: 
	add	a0,zero,a1
	addi	a0,a0,2
	j	lambda_0_conclusion
	j	lambda_0_conclusion
lambda_0_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,16
	ret

	.globl	main
	.align	8
main: 
	addi	sp,sp,-144
	sd	zero,32(sp)
	sd	zero,24(sp)
	sd	zero,16(sp)
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,136(sp)
	sd	fp,128(sp)
	addi	fp,sp,144
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
	li	t0,20
	sd	t0,-120(fp)
	li	t0,200
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,24
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_4
	j	orelse_5
body_4: 
	j	cont_6
cont_6: 
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	a0,t0,1
	la	t0,gc_free_ptr
	ld	t0,0(t0)
	addi	t0,t0,24
	la	t1,gc_free_ptr
	sd	t0,0(t1)
	li	t0,4
	sd	t0,-1(a0)
	ld	t0,-120(fp)
	sd	t0,7(a0)
	ld	t0,-112(fp)
	sd	t0,15(a0)
	add	t0,zero,a0
	sd	t0,-112(fp)
	la	t0,map
	sd	t0,-120(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_7
	j	orelse_8
body_7: 
	j	cont_9
cont_9: 
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
	ld	t0,-120(fp)
	sd	t0,7(a0)
	add	t0,zero,a0
	sd	t0,-120(fp)
	ld	t0,-120(fp)
	ld	t0,7(t0)
	sd	t0,-136(fp)
	la	t0,lambda_0
	sd	t0,-128(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_10
	j	orelse_11
body_10: 
	j	cont_12
cont_12: 
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
	add	a1,zero,a0
	ld	t0,-128(fp)
	sd	t0,7(a1)
	ld	a0,-120(fp)
	ld	a2,-112(fp)
	ld	t0,-136(fp)
	jalr	t0
	add	s1,zero,a0
	ld	a0,-112(fp)
	ld	a0,7(a0)
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	ld	a0,-112(fp)
	ld	a0,15(a0)
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	ld	a0,7(s1)
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	ld	a0,15(s1)
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
	addi	sp,sp,144
	addi	a0,zero,0
	ret
orelse_11: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_12
orelse_8: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_9
orelse_5: 
	add	a0,zero,sp
	li	a1,3
	call	gc_collect
	j	cont_6