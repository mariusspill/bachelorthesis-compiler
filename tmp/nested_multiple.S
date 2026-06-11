
	.globl	Vector3D
	.align	8
Vector3D: 
	addi	sp,sp,-48
	sd	zero,24(sp)
	sd	zero,16(sp)
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,40(sp)
	sd	fp,32(sp)
	addi	fp,sp,48
	j	Vector3D_start
Vector3D_start: 
	add	a0,zero,a1
	add	a1,zero,a2
	add	a2,zero,a3
	add	t0,zero,a0
	sd	t0,-40(fp)
	add	t0,zero,a1
	sd	t0,-24(fp)
	add	t0,zero,a2
	sd	t0,-32(fp)
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
	ld	t0,-40(fp)
	sd	t0,7(a0)
	ld	t0,-24(fp)
	sd	t0,15(a0)
	ld	t0,-32(fp)
	sd	t0,23(a0)
	j	Vector3D_conclusion
	j	Vector3D_conclusion
Vector3D_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,48
	ret
orelse_1: 
	add	a0,zero,sp
	li	a1,4
	call	gc_collect
	j	cont_2

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
	add	a1,zero,a2
	add	a2,zero,a3
	add	t0,zero,a0
	sd	t0,-32(fp)
	add	t0,zero,a1
	sd	t0,-40(fp)
	add	t0,zero,a2
	sd	t0,-24(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,32
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_3
	j	orelse_4
body_3: 
	j	cont_5
cont_5: 
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
orelse_4: 
	add	a0,zero,sp
	li	a1,4
	call	gc_collect
	j	cont_5

	.globl	Color
	.align	8
Color: 
	addi	sp,sp,-32
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,24(sp)
	sd	fp,16(sp)
	addi	fp,sp,32
	j	Color_start
Color_start: 
	add	a0,zero,a1
	add	a1,zero,a2
	add	t0,zero,a0
	sd	t0,-32(fp)
	add	t0,zero,a1
	sd	t0,-24(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,24
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_6
	j	orelse_7
body_6: 
	j	cont_8
cont_8: 
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
	ld	t0,-32(fp)
	sd	t0,7(a0)
	ld	t0,-24(fp)
	sd	t0,15(a0)
	j	Color_conclusion
	j	Color_conclusion
Color_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	ret
orelse_7: 
	add	a0,zero,sp
	li	a1,3
	call	gc_collect
	j	cont_8

	.globl	Light
	.align	8
Light: 
	addi	sp,sp,-48
	sd	zero,24(sp)
	sd	zero,16(sp)
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,40(sp)
	sd	fp,32(sp)
	addi	fp,sp,48
	j	Light_start
Light_start: 
	add	a0,zero,a1
	add	a1,zero,a2
	add	a2,zero,a3
	add	t0,zero,a0
	sd	t0,-32(fp)
	add	t0,zero,a1
	sd	t0,-40(fp)
	add	t0,zero,a2
	sd	t0,-24(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,32
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
	j	Light_conclusion
	j	Light_conclusion
Light_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,48
	ret
orelse_10: 
	add	a0,zero,sp
	li	a1,4
	call	gc_collect
	j	cont_11

	.globl	r_intensity
	.align	8
r_intensity: 
	addi	sp,sp,-16
	sd	ra,8(sp)
	sd	fp,0(sp)
	addi	fp,sp,16
	j	r_intensity_start
r_intensity_start: 
	add	a2,zero,a1
	ld	a0,7(a2)
	ld	a1,15(a2)
	add	a0,a0,a1
	ld	a1,23(a2)
	add	a0,a0,a1
	j	r_intensity_conclusion
	j	r_intensity_conclusion
r_intensity_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,16
	ret

	.globl	c_intensity
	.align	8
c_intensity: 
	addi	sp,sp,-32
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,24(sp)
	sd	fp,16(sp)
	addi	fp,sp,32
	j	c_intensity_start
c_intensity_start: 
	add	t0,zero,a1
	sd	t0,-24(fp)
	la	t0,r_intensity
	sd	t0,-32(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_12
	j	orelse_13
body_12: 
	j	cont_14
cont_14: 
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
	ld	t0,-32(fp)
	sd	t0,7(a0)
	ld	a2,7(a0)
	ld	a1,-24(fp)
	ld	a1,7(a1)
	jalr	a2
	ld	a1,-24(fp)
	ld	a1,15(a1)
	add	a0,a0,a1
	j	c_intensity_conclusion
	j	c_intensity_conclusion
c_intensity_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	ret
orelse_13: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_14

	.globl	l_intensity
	.align	8
l_intensity: 
	addi	sp,sp,-32
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,24(sp)
	sd	fp,16(sp)
	addi	fp,sp,32
	j	l_intensity_start
l_intensity_start: 
	add	t0,zero,a1
	sd	t0,-32(fp)
	la	t0,c_intensity
	sd	t0,-24(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_15
	j	orelse_16
body_15: 
	j	cont_17
cont_17: 
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
	ld	t0,-24(fp)
	sd	t0,7(a0)
	ld	a2,7(a0)
	ld	a1,-32(fp)
	ld	a1,23(a1)
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	jr	a2, 0
	j	l_intensity_conclusion
l_intensity_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	ret
orelse_16: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_17

	.globl	v_add
	.align	8
v_add: 
	addi	sp,sp,-48
	sd	zero,24(sp)
	sd	zero,16(sp)
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,40(sp)
	sd	fp,32(sp)
	addi	fp,sp,48
	j	v_add_start
v_add_start: 
	add	t0,zero,a1
	sd	t0,-32(fp)
	add	t0,zero,a2
	sd	t0,-40(fp)
	la	t0,Vector3D
	sd	t0,-24(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_18
	j	orelse_19
body_18: 
	j	cont_20
cont_20: 
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
	ld	t0,-24(fp)
	sd	t0,7(a0)
	ld	a4,7(a0)
	ld	a1,-32(fp)
	ld	a1,7(a1)
	ld	a2,-40(fp)
	ld	a2,7(a2)
	add	a1,a1,a2
	ld	a2,-32(fp)
	ld	a2,15(a2)
	ld	a3,-40(fp)
	ld	a3,15(a3)
	add	a2,a2,a3
	ld	a3,-32(fp)
	ld	a3,23(a3)
	ld	a5,-40(fp)
	ld	a5,23(a5)
	add	a3,a3,a5
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,48
	jr	a4, 0
	j	v_add_conclusion
v_add_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,48
	ret
orelse_19: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_20

	.globl	v_print
	.align	8
v_print: 
	addi	sp,sp,-32
	sd	zero,0(sp)
	sd	ra,24(sp)
	sd	fp,16(sp)
	addi	fp,sp,32
	sd	s1,-24(fp)
	j	v_print_start
v_print_start: 
	add	s1,zero,a1
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
	li	a0,0
	j	v_print_conclusion
	j	v_print_conclusion
v_print_conclusion: 
	ld	s1,-24(fp)
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	ret

	.globl	l_target
	.align	8
l_target: 
	addi	sp,sp,-32
	sd	zero,8(sp)
	sd	zero,0(sp)
	sd	ra,24(sp)
	sd	fp,16(sp)
	addi	fp,sp,32
	j	l_target_start
l_target_start: 
	add	t0,zero,a1
	sd	t0,-24(fp)
	la	t0,v_add
	sd	t0,-32(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_21
	j	orelse_22
body_21: 
	j	cont_23
cont_23: 
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
	ld	t0,-32(fp)
	sd	t0,7(a0)
	ld	a3,7(a0)
	ld	a1,-24(fp)
	ld	a1,7(a1)
	ld	a2,-24(fp)
	ld	a2,15(a2)
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	jr	a3, 0
	j	l_target_conclusion
l_target_conclusion: 
	ld	ra,-8(fp)
	ld	fp,-16(fp)
	addi	sp,sp,32
	ret
orelse_22: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_23

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
	la	t0,Vector3D
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_24
	j	orelse_25
body_24: 
	j	cont_26
cont_26: 
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
	li	a1,20
	li	a2,40
	li	a3,60
	jalr	a4
	add	t0,zero,a0
	sd	t0,-120(fp)
	la	t0,Vector3D
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_27
	j	orelse_28
body_27: 
	j	cont_29
cont_29: 
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
	li	a1,6
	li	a2,4
	li	a3,2
	jalr	a4
	add	t0,zero,a0
	sd	t0,-136(fp)
	la	t0,RGB
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_30
	j	orelse_31
body_30: 
	j	cont_32
cont_32: 
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
	add	t0,zero,a0
	sd	t0,-112(fp)
	la	t0,Color
	sd	t0,-128(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_33
	j	orelse_34
body_33: 
	j	cont_35
cont_35: 
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
	ld	t0,-128(fp)
	sd	t0,7(a0)
	ld	a3,7(a0)
	ld	a1,-112(fp)
	li	a2,200
	jalr	a3
	add	t0,zero,a0
	sd	t0,-128(fp)
	la	t0,Light
	sd	t0,-144(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_36
	j	orelse_37
body_36: 
	j	cont_38
cont_38: 
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
	ld	t0,-144(fp)
	sd	t0,7(a0)
	ld	a4,7(a0)
	ld	a1,-120(fp)
	ld	a2,-136(fp)
	ld	a3,-128(fp)
	jalr	a4
	add	t0,zero,a0
	sd	t0,-120(fp)
	la	t0,r_intensity
	sd	t0,-136(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_39
	j	orelse_40
body_39: 
	j	cont_41
cont_41: 
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
	ld	t0,-136(fp)
	sd	t0,7(a0)
	ld	a2,7(a0)
	ld	a1,-112(fp)
	jalr	a2
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	la	t0,c_intensity
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_42
	j	orelse_43
body_42: 
	j	cont_44
cont_44: 
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
	ld	a2,7(a0)
	ld	a1,-128(fp)
	jalr	a2
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	la	t0,l_intensity
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_45
	j	orelse_46
body_45: 
	j	cont_47
cont_47: 
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
	ld	a2,7(a0)
	ld	a1,-120(fp)
	jalr	a2
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	li	a0,0
	li	t1,2
	div	a0,a0,t1
	call	print_int64
	la	t0,v_print
	sd	t0,-112(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a1,a0,16
	la	a0,gc_fromspace_end
	ld	a0,0(a0)
	blt	a1,a0,body_48
	j	orelse_49
body_48: 
	j	cont_50
cont_50: 
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
	add	t0,zero,a0
	sd	t0,-128(fp)
	ld	t0,-128(fp)
	ld	t0,7(t0)
	sd	t0,-112(fp)
	la	t0,l_target
	sd	t0,-136(fp)
	la	a0,gc_free_ptr
	ld	a0,0(a0)
	addi	a0,a0,16
	la	a1,gc_fromspace_end
	ld	a1,0(a1)
	blt	a0,a1,body_51
	j	orelse_52
body_51: 
	j	cont_53
cont_53: 
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
	ld	t0,-136(fp)
	sd	t0,7(a0)
	ld	a2,7(a0)
	ld	a1,-120(fp)
	jalr	a2
	add	a1,zero,a0
	ld	a0,-128(fp)
	ld	t0,-112(fp)
	jalr	t0
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
orelse_52: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_53
orelse_49: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_50
orelse_46: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_47
orelse_43: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_44
orelse_40: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_41
orelse_37: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_38
orelse_34: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_35
orelse_31: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_32
orelse_28: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_29
orelse_25: 
	add	a0,zero,sp
	li	a1,2
	call	gc_collect
	j	cont_26