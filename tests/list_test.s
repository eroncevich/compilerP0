.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $8, %esp
	movl $5, -4(%ebp)
	movl $1, %eax
	pushl $3
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call create_list
	addl $4, %esp
	movl %eax,%edi
	pushl %edi
	call inject_big
	addl $4, %esp
	movl %eax,%ebx
	pushl $0
	call inject_int
	addl $4, %esp
	movl %eax,%esi
	pushl $4
	pushl %esi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	addl $4, %esp
	movl %eax,%esi
	pushl $8
	pushl %esi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	addl $4, %esp
	movl %eax,%esi
	pushl $12
	pushl %esi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl %edi
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %esi
	cmp %esi, %esi
	jne ne_cmp0
	movl $1, %edi
	jmp end_cmp0
	ne_cmp0:
	movl $0, %edi
	end_cmp0:
	pushl %edi
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call print_any
	popl %ebx
	pushl $3
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call create_list
	addl $4, %esp
	movl %eax,-8(%ebp)
	pushl -8(%ebp)
	call inject_big
	addl $4, %esp
	movl %eax,%edi
	pushl $0
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl $4
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl $8
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl $12
	pushl %ebx
	pushl %edi
	call set_subscript
	addl $12, %esp
	pushl -8(%ebp)
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	cmp %esi, %eax
	jne ne_cmp1
	movl $1, %ebx
	jmp end_cmp1
	ne_cmp1:
	movl $0, %ebx
	end_cmp1:
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call print_any
	popl %esi
	call create_dict
	addl $0, %esp
	movl %eax,%ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%esi
	pushl $8
	pushl $4
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl $12
	pushl $8
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	cmp %eax, %eax
	jne ne_cmp2
	movl $1, %ebx
	jmp end_cmp2
	ne_cmp2:
	movl $0, %ebx
	end_cmp2:
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call print_any
	popl %esi
	movl $8, %edi
	movl $8, %eax
	cmp %edi, %eax
	jne ne_cmp3
	movl $1, %ebx
	jmp end_cmp3
	ne_cmp3:
	movl $0, %ebx
	end_cmp3:
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call print_any
	popl %esi
	movl $8, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $48, %ebx
	sarl $2, %ebx
	movl $40, %eax
	sarl $2, %eax
	movl %eax, %esi
	negl %esi
	pushl %esi
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	cmp %edi, %eax
	jne ne_cmp4
	movl $1, %esi
	jmp end_cmp4
	ne_cmp4:
	movl $0, %esi
	end_cmp4:
	pushl %esi
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call print_any
	popl %ebx
	movl $4, %eax
	cmp -4(%ebp), %eax
	jne ne_cmp5
	movl $1, %ebx
	jmp end_cmp5
	ne_cmp5:
	movl $0, %ebx
	end_cmp5:
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call print_any
	popl %esi
	movl -4(%ebp), %eax
	cmp %eax, -4(%ebp)
	jne ne_cmp6
	movl $1, %ebx
	jmp end_cmp6
	ne_cmp6:
	movl $0, %ebx
	end_cmp6:
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call print_any
	popl %esi
	pushl $3
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call create_list
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	call inject_big
	addl $4, %esp
	movl %eax,%ebx
	pushl $0
	call inject_int
	addl $4, %esp
	movl %eax,%edi
	pushl $0
	pushl %edi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	addl $4, %esp
	movl %eax,%edi
	pushl $4
	pushl %edi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	addl $4, %esp
	movl %eax,%edi
	pushl $8
	pushl %edi
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl %esi
	call inject_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call project_big
	addl $4, %esp
	movl %eax,%edi
	pushl $3
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call create_list
	addl $4, %esp
	movl %eax,-4(%ebp)
	pushl -4(%ebp)
	call inject_big
	addl $4, %esp
	movl %eax,%esi
	pushl $0
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl $12
	pushl %ebx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl $1
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl $16
	pushl %ebx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl $2
	call inject_int
	addl $4, %esp
	movl %eax,%ebx
	pushl $20
	pushl %ebx
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl -4(%ebp)
	call inject_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call project_big
	addl $4, %esp
	movl %eax,%esi
	pushl %esi
	pushl %edi
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	call create_dict
	addl $0, %esp
	movl %eax,%ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %ebx
	movl $4, %esi
	pushl %esi
	pushl $0
	pushl %ebx
	call set_subscript
	addl $12, %esp
	movl $8, %esi
	pushl %esi
	pushl $4
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $0
	pushl %ebx
	call get_subscript
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %edi
	pushl $4
	pushl %ebx
	call get_subscript
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %esi
	movl %edi, %eax
	andl $3, %eax
	sarl $1, %eax
	cmp $0, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then0
	movl %edi, %eax
	andl $3, %eax
	cmp $3, %eax
	movl $1, %eax
	movl $0, %ebx
	cmove %eax, %ebx
	pushl %ebx
	call inject_bool
	addl $4, %esp
	movl %eax,%ebx
	pushl %ebx
	call is_true
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	movl %eax, %eax
	cmp $0, %eax
	jne then1
	movl $777777, %eax
	jmp end1
	then1:
	pushl %edi
	call project_big
	addl $4, %esp
	movl %eax,%ebx
	pushl %esi
	call project_big
	addl $4, %esp
	movl %eax,%edi
	pushl %edi
	pushl %ebx
	call add
	addl $8, %esp
	movl %eax,%eax
	movl %eax, %ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end1:
	movl %eax, %eax
	jmp end0
	then0:
	movl %edi, %ebx
	sarl $2, %ebx
	movl %esi, %eax
	sarl $2, %eax
	movl %ebx, %ebx
	addl %eax, %ebx
	pushl %ebx
	call inject_int
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %eax
	end0:
	movl %eax, %eax
	movl %eax, %ebx
	pushl %ebx
	call print_any
	popl %ebx
	call create_dict
	addl $0, %esp
	movl %eax,%ebx
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%esi
	pushl $0
	pushl $4
	pushl %esi
	call set_subscript
	addl $12, %esp
	pushl %ebx
	call inject_big
	addl $4, %esp
	movl %eax,%eax
	movl %eax, %ebx
	movl $28, %esi
	pushl %esi
	pushl $4
	pushl %ebx
	call set_subscript
	addl $12, %esp
	pushl $4
	pushl %ebx
	call get_subscript
	addl $8, %esp
	movl %eax,%esi
	pushl %esi
	call print_any
	popl %esi
	movl $0,%eax
	leave
	ret
