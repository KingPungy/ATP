.cpu cortex-m0
.align 2

.text
.global even

even:
push { r4, r5, r6, r7, lr }
mov r4, r0
mov r5, #1
mov r6, #1
mov r0, r4
mov r1, #0
cmp r0, r1
bne ifEnd_49bb97a80d
mov r0, #1
sub r5, r5, r0
ifEnd_49bb97a80d:
mov r0, r5
mov r1, #1
cmp r0, r1
bne ifEnd_03981088a1
mov r0, #1
sub r4, r4, r0
mov r0, r4
bl odd
mov r7, r0
mov r0, #1
sub r6, r6, r0
add r6, r6, r7
ifEnd_03981088a1:
mov r0, r6
pop { r4, r5, r6, r7, pc }
