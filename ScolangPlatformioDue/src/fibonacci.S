.cpu cortex-m0
.align 2

.text
.global fibonacci

fibonacci:
push { r4, r5, r6, r7, lr }
mov r4, r0
mov r5, #0
mov r6, #0
mov r0, r4
mov r1, #0
cmp r0, r1
bne ifEnd_fdcee29d31
mov r7, #1
mov r5, r4
ifEnd_fdcee29d31:
mov r0, r4
mov r1, #1
cmp r0, r1
bne ifEnd_e12985e531
mov r6, #1
mov r7, r4
ifEnd_e12985e531:
mov r0, r6
mov r1, #0
cmp r0, r1
bne ifEnd_882d250677
whileBegin_0845ef276f:
mov r0, r6
mov r1, #2
cmp r0, r1
beq whileEnd_0845ef276f
mov r0, #1
sub r4, r4, r0
mov r0, r4
bl fibonacci
mov r5, r0
add r7, r7, r5
mov r0, #1
add r6, r6, r0
b whileBegin_0845ef276f
whileEnd_0845ef276f:
ifEnd_882d250677:
mov r0, r7
pop { r4, r5, r6, r7, pc }
