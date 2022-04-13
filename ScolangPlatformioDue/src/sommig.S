.cpu cortex-m0
.align 2

.text
.global sommig

sommig:
push { r4, r5, lr }
mov r4, r0
mov r5, #0
whileBegin_63e2e4f852:
mov r0, r4
mov r1, #0
cmp r0, r1
beq whileEnd_63e2e4f852
add r5, r5, r4
mov r0, #1
sub r4, r4, r0
b whileBegin_63e2e4f852
whileEnd_63e2e4f852:
mov r0, r5
pop { r4, r5, pc }
